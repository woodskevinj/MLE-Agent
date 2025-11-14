"""
Explainability Tools (SHAP)
---------------------------
Computes and visualizes model explainability insights:
- Global feature importance
- Local (per-sample) explanations
"""

import os
import shap
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# simple global cache (shared across tool calls)
_GLOBAL_CACHE = {}


def compute_shap_values(state):
    """
    Compute SHAP values for the cached model and dataframe.
    Supports: LogisticRegression, RandomForestClassifier
    Stores shap_values and explainer in the state
    """
    model = state.get("model")
    df = state.get("df")

    if model is None or df is None:
        return "Model or dataframe not found.  Train model and load datafame first."
    
    # ensure consistent feature matrix
    X = df.drop(columns=["Churn"], errors="ignore")
    X = X.select_dtypes(include=[np.number])

    try:
        # choose explainer type based on model class
        if "LogisticRegression" in str(type(model)):
            explainer = shap.LinearExplainer(model, X, feature_perturbation="interventional")
        else:
            explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X)
        state["shap_values"] = shap_values
        state["explainer"] = explainer
        state["X"] = X

        return f"SHAP values computed for {X.shape[0]} samples and {X.shape[1]} features."
    
    except Exception as e:
        return f"Error computing SHAP values: {e}"
    

def plot_global_importance(state, top_n: int = 10):
    """
    Plot global feature importance based on mean(|SHAP|) values.
    Saves plot to images/shap_global.png
    """
    shap_values = state.get("shap_values")
    X = state.get("X")

    if shap_values is None or X is None:
        return "No SHAP values found. Run compute_shap_values() first."
    
    os.makedirs("images", exist_ok=True)

    try:
        # compute mean absolute shap values
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        importance = pd.Series(mean_abs_shap, index=X.columns).sort_values(ascending=False)
        top_features = importance.head(top_n)

        plt.figure(figsize=(8, 6))
        top_features[::-1].plot(kind="barh")
        plt.title(f"Top {top_n} Feature Importances (mean |SHAP|)")
        plt.xlabel("Mean |SHAP value|")
        plt.tight_layout()
        plt.savefig("images/shap_global.png")

        return f"Global SHAP importance plot saved to images/shap_global.png"
    
    except Exception as e:
        return f"Error plotting global SHAP: {e}"
    

def plot_local_explanation(state, row_index: int = 0):
    """
    Plot a single instances's SHAP explanation (force plot style).
    Saves a plot to images/shap_local.png
    """
    explainer = state.get("explainer")
    shap_values = state.get("shap_values")
    X = state.get("X")

    if explainer is None or shap_values is None or X is None:
        return "Missing SHAP data. Run compute_shap_values() first."
    
    os.makedirs("images", exist_ok=True)

    try:
        row = X.iloc[[row_index]]
        shap_value = shap_values[row_index]

        plt.figure(figsize=(8, 4))
        shap.plots.waterfall(shap.Explanation(values=shap_value, base_values=explainer.expected_value, data=row.iloc[0].values, feature_names=row.columns), show=False)
        plt.tight_layout()
        plt.savefig("images/shap_local.png", bbox_inches="tight")

        return f"Local SHAP explanation saved to images/shap_local.png"
    
    except Exception as e:
        return f"Error plotting local SHAP explanation: {e}"
