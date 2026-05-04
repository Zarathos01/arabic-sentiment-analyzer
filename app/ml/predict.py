import numpy as np
from ml.preprocessing import preprocess_text 


LABEL_MAPPING = {0: 'Negative', 1: 'Positive'}


def predict_sentiment(model, vectorizer, text: str) -> str:
    if not text or not text.strip():
        return "unknown"

    cleaned_text = preprocess_text(text)

    if not cleaned_text.strip():
        return "unknown"

    text_vector = vectorizer.transform([cleaned_text])
    prediction = model.predict(text_vector)

    # model.predict() returns a numpy array — extract the scalar value
    label_index = int(prediction[0])

    return LABEL_MAPPING.get(label_index, "unknown")


def predict_batch(model, vectorizer, texts: list[str]) -> list[str]:
    """
    Predict sentiment for a list of texts in one vectorizer call (efficient).
    Returns a list of label strings in the same order as input.
    """
    if not texts:
        return []

    cleaned = [preprocess_text(t) for t in texts]
    # Filter empties but preserve positions
    valid_indices = [i for i, t in enumerate(cleaned) if t.strip()]
    valid_texts = [cleaned[i] for i in valid_indices]

    results = ["unknown"] * len(texts)

    if valid_texts:
        vectors = vectorizer.transform(valid_texts)
        predictions = model.predict(vectors)
        for i, pred in zip(valid_indices, predictions):
            results[i] = LABEL_MAPPING.get(int(pred), "unknown")

    return results