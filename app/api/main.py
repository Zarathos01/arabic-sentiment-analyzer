import sys
import os
from contextlib import asynccontextmanager
from typing import Optional
import io

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ml.model_loader import load_model, load_vectorizer
from ml.predict import predict_sentiment, predict_batch


# ── App state ─────────────────────────────────────────────────────────────────

class AppState:
    model = None
    vectorizer = None

state = AppState()


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    state.model = load_model()
    state.vectorizer = load_vectorizer()
    yield


app = FastAPI(
    title="Arabic Sentiment Analyzer API",
    description="Analyze and predict the sentiment of Arabic comments and replies.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Schemas ───────────────────────────────────────────────────────────────────

class TextRequest(BaseModel):
    text: str

class SentimentResult(BaseModel):
    text: str
    sentiment: str

class BatchResponse(BaseModel):
    total: int
    results: list[SentimentResult]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": state.model is not None,
        "vectorizer_loaded": state.vectorizer is not None,
    }


@app.post("/predict", response_model=SentimentResult)
def predict(request: TextRequest):
    """Predict sentiment for a single Arabic text."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty.")
    sentiment = predict_sentiment(state.model, state.vectorizer, request.text)
    return SentimentResult(text=request.text, sentiment=sentiment)


@app.post("/predict/csv", response_model=BatchResponse)
async def predict_csv(
    file: UploadFile = File(...),
    column: Optional[str] = None,
):
    
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {e}")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV file is empty.")

    # Auto-detect column
    if column is None:
        if len(df.columns) == 1:
            column = df.columns[0]
        else:
            # Try common column names
            common = ["text", "comment", "reply", "review", "نص", "تعليق", "مراجعة"]
            matched = [c for c in df.columns if c.strip().lower() in common]
            if matched:
                column = matched[0]
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Multiple columns found: {list(df.columns)}. Pass ?column=your_column_name to specify which one contains the text."
                )

    if column not in df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{column}' not found. Available columns: {list(df.columns)}"
        )

    texts = df[column].dropna().astype(str).tolist()
    if not texts:
        raise HTTPException(status_code=400, detail="No text found in the specified column.")

    sentiments = predict_batch(state.model, state.vectorizer, texts)
    results = [SentimentResult(text=t, sentiment=s) for t, s in zip(texts, sentiments)]

    return BatchResponse(total=len(results), results=results)