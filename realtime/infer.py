# realtime/infer.py
import joblib

def load_model():
    model = joblib.load("model/ids_model.pkl")
    return model

def predict(model, X):
    """
    Args:
        model: trained IDS model
        X: preprocessed feature matrix
    Returns:
        predictions: 0 (benign) or 1 (attack)
    """
    predictions = model.predict(X)
    return predictions
