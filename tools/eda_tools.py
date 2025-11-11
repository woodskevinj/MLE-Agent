"""
EDA Tools: lightweight utilities for dataset exploration
"""

import pandas as pd
from typing import Optional


def load_csv(state, path: str) -> str:
    """
    Load a CSV file and return a quick summary
    - shape
    - column list
    Saves the dataframe to memory (global cache).
    """
    try:
        df = pd.read_csv(path)
        state["df"] = df
    except Exception as e:
        return f"Error loading CSV: {e}"

    return (
        f"CSV loaded successfully.\n"
        f"Shape: {df.shape}\n"
        f"Columns: {list(df.columns)}"
    )

def preview_data(state, n: int = 5) -> str:
    """
    Return the top n rows as a string.
    Requires that load_csv() was called first.
    """
    df = state.get("df")

    if df is None:
        return "No datafram loaded. Use load_csv <path> first."
    
    return df.head(n).to_string()

def describe_data(state) -> str:
    """
    Returns summary statistics, missing counts, and dtypes.
    """
    df = state.get("df")
    if df is None:
        return "No dataframe loaded.  Use load_csv <path> first."
    
    desc = df.describe(include='all').to_string()
    missing = df.isna().sum().to_string()
    dtypes = df.dtypes.to_string()

    return (
        f"Summary Statistics:\n{desc}\n\n"
        f"Missing Values:\n{missing}\n\n"
        f"Columne Types:\n{dtypes}"
    )


def column_info(state) -> str:
    """
    Returns column classification:
    - numerical columns
    - categorical columns
    """
    df = state.get("df")
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    numerical = df.select_dtypes(include=['number']).columns.tolist()
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()

    return (
        f"Numerical Columns: {numerical}\n"
        f"Categorical Columns: {categorical}"
    )

