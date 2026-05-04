# 🧠 Arabic Sentiment Analyzer

A machine learning web application that analyzes the sentiment of Arabic text. Upload a CSV file of comments or replies, or type a single text, and get instant positive/negative predictions powered by a trained Arabic NLP model.

---

## 📸 Features

- **CSV Upload** — Upload any CSV file with Arabic comments and get batch sentiment predictions
- **Single Text Analysis** — Type or paste any Arabic text and get an instant result
- **Visual Results** — Color-coded cards, sentiment split bar, and stats summary
- **Download Results** — Export predictions as a CSV file
- **REST API** — FastAPI backend with interactive docs at `/docs`

---

## 🗂️ Project Structure

```
project/
│
├── app/
│   ├── api/
│   │   └── main.py               # FastAPI app — endpoints & lifespan
│   │
│   ├── ml/
│   │   ├── preprocessing.py      # Arabic text cleaning & normalization
│   │   ├── predict.py            # Sentiment prediction logic
│   │   └── model_loader.py       # Load model & vectorizer from disk
│   │
│   └── utils/
│
├── models/
│   ├── sentiment_model.pkl       # Trained ML model
│   └── tfidf_vectorizer.pkl      # Fitted TF-IDF vectorizer
│
├── streamlit_app/
│   └── app.py                    # Streamlit frontend
│
├── notebooks/                    # Training & experimentation notebooks
├── requirements.txt
├── README.md
├── .gitignore
└── Dockerfile
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/arabic-sentiment-analyzer.git
cd arabic-sentiment-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 5. Add your trained models

Place your trained model and vectorizer in the `models/` folder:

```
models/
├── sentiment_model.pkl
└── tfidf_vectorizer.pkl
```

> If you don't have trained models yet, run the notebooks in `notebooks/` to train and export them.

---

## 🚀 Running the App

You need **two terminals** running at the same time.

### Terminal 1 — Start the API

```bash
cd app/api
uvicorn main:app --reload --port 8001
```

The API will be available at `http://127.0.0.1:8001`  
Interactive API docs at `http://127.0.0.1:8001/docs`

### Terminal 2 — Start the Streamlit frontend

```bash
streamlit run streamlit_app/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check if the API and models are loaded |
| `POST` | `/predict` | Predict sentiment for a single text |
| `POST` | `/predict/csv` | Upload a CSV file for batch prediction |

### `/predict` — Single text

```bash
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "المنتج رائع جداً"}'
```

```json
{
  "text": "المنتج رائع جداً",
  "sentiment": "Positive"
}
```

### `/predict/csv` — CSV batch

```bash
curl -X POST "http://127.0.0.1:8001/predict/csv" \
  -F "file=@comments.csv" \
  -F "column=text"
```

```json
{
  "total": 120,
  "results": [
    {"text": "...", "sentiment": "Positive"},
    {"text": "...", "sentiment": "Negative"}
  ]
}
```

---

## 📄 CSV Format

Your CSV file should have at least one column containing Arabic text:

```csv
comment
المنتج ممتاز وسريع التوصيل
الجودة سيئة جداً ولن أشتري مرة أخرى
خدمة العملاء متعاونة جداً
```

If your CSV has multiple columns, the app will ask you to select which column to analyze.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| ML Model | Scikit-learn (Logistic Regression) |
| Text Processing | NLTK, regex, emoji |
| API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Serialization | Joblib |

---

## 📦 Requirements

Key dependencies (see `requirements.txt` for full list):

```
fastapi
uvicorn
streamlit
scikit-learn
pandas
nltk
emoji
joblib
pydantic
```

---

## 📝 License

This project is for educational purposes.