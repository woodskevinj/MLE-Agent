"""
Feature Engineering Tools

-------------------------
These utilities operate on the dataframe currently cached by load_csv().
They transform the dataframe in-place inside the global cache.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import json


# -------------------------------------------------------
# Train/Test Split
# -------------------------------------------------------
def split_data(state, label="Churn", test_size = 0.2):
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    X = df.drop(label, axis=1)
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    state["train"] = (X_train, y_train)
    state["test"] = (X_test, y_test)

    return "Data split into train/test sets."
    

# -------------------------------------------------------
# Encode categoricals
# -------------------------------------------------------
def encode_categoricals(state):
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    cat_cols = [
        col for col in df.select_dtypes(include=["object"]).columns
        if col != "Churn" and df[col].nunique() < 50
    ]

    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    state["df"] = df_encoded
    return f"Categoricals encoded. New shape: {df_encoded.shape}"
    

# -------------------------------------------------------
# Scale numeric features
# -------------------------------------------------------
def scale_numericals(state):
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    state["df"] = df
    return f"Numerical features scaled ({len(num_cols)} columns)."
    

# -------------------------------------------------------
# Save dataframe
# -------------------------------------------------------
def save_dataframe(state, path):
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    df.to_csv(path, index=False)
    return f"DataFrame saved to {path}"

    