"""
ML Training Tools
-----------------
Provides utilities for supervised model training and evaluation.
Works on the dataframe cached in Feature / EDA tools
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import joblib
import os


# simple global cache (shared session state)
_GLOBAL_CACHE = {}


def get_df():
    df = _GLOBAL_CACHE.get("df")
    if df is None:
        return None, "No dataframe loaded. Use load_csv <path> first."
    return df, None

# ----------------------------------------------------------
# Train a baseline model
# ----------------------------------------------------------
def train_model(state, label="Churn", model_type="logistic"):
    """
    Train a baseline model on the cached dataframe
    Supports: logistic | random_forest
    Saves a model + metrics to state.
    """
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    if label not in df.columns:
        return f"Label column '{label}' not found."
    
    model_type = model_type.lower().strip()
    
    # Split features/target
    X = df.drop(label, axis=1)
    y = df[label]

    # Drop non-numeric columns (e.g. IDs left from earlier)
    X = X.select_dtypes(include=["number"])

    # If y is categorical string, encode
    if y.dtype == "O":
        y = (y.str.lower().str.strip().isin(["yes", "true", "1", "churned", "positive"])).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "logistic":
        model = LogisticRegression(max_iter=500)
    elif model_type in ["rf", "random_forest", "randomforest"]:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        return f"Unknown model_type '{model_type}'."
    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)
    cm = confusion_matrix(y_test, preds)

    # Cache results
    state["model"] = model
    state["metrics"] = {"accuracy": acc, "report": report}
    state["confusion_matrix"] = cm.tolist()

    return (
        f"Model trained successfully ({model_type}).\n"
        f"Accuracy: {acc:.4f}\n"
        f"Confusion Matrix:\n{cm}\n"
        f"Classification Report:\n{report}"
    )

# ----------------------------------------------------------
# Evaluate model (reload or reuse)
# ----------------------------------------------------------
def evaluate_model(state, path=None):
    """
    Evaluate the cached or reloaded model on cached test data
    """
    model = state.get("model")
    if model is None:
        if path and os.path.exists(path):
            model = joblib.load(path)
        else:
            return "No model loaded or provided path invalided."
        
    test_data = state.get("test")
    if not test_data:
        return "No cached test set found. Use split_data() before training."
    
    X_test, y_test = test_data
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)
    return f"Evaluation complete.\nAccuracy: {acc:.4f}\n\n{report}"

# ----------------------------------------------------------
# Save model
# ----------------------------------------------------------
def save_model(state, path="model.pkl"):
    model = state.get("model")
    if model is None:
        return "No model cached. Train a model first."
    
    # ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    joblib.dump(model, path)
    return f"Model saved to {path}"
