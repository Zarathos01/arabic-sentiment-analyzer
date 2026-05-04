import joblib
import os

# Base path: go up two levels from app/ml/ to reach project root, then into models/
_PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
_MODELS_DIR = os.path.join(_PROJECT_ROOT, "models")


def load_model(model_path=None):
    if model_path is None:
        model_path = os.path.join(_MODELS_DIR, "sentiment_model.pkl")
    model_path = os.path.abspath(model_path)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    return joblib.load(model_path)


def load_vectorizer(vectorizer_path=None):
    if vectorizer_path is None:
        vectorizer_path = os.path.join(_MODELS_DIR, "tfidf_vectorizer.pkl")
    vectorizer_path = os.path.abspath(vectorizer_path)
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found at: {vectorizer_path}")
    return joblib.load(vectorizer_path)