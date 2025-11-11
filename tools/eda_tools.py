"""
EDA Tools: lightweight utilities for dataset exploration
"""

import pandas as pd
from typing import Optional


def load_csv(path: str) -> str:
    """
    Load a CSV file and return a quick summary
    - shape
    - column list
    Saves the dataframe to memory (global cache).
    """
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"Error loading CSV: {e}"
    
    # Store in global cache for later tools
    _GLOBAL_CACHE['df'] = df

    return (
        f"CSV loaded successfully.\n"
        f"Shape: {df.shape}\n"
        f"Columns: {list(df.columns)}"
    )

def preview_data(n: int = 5) -> str:
    """
    Return the top n rows as a string.
    Requires that load_csv() was called first.
    """
    df = _GLOBAL_CACHE.get('df')
    if df is None:
        return "No datafram loaded. Use load_csv <path> first."
    
    return df.head(n).to_string()

def describe_data() -> str:
    """
    Returns summary statistics, missing counts, and dtypes.
    """
    df = _GLOBAL_CACHE.get('df')
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


def column_info() -> str:
    """
    Returns column classification:
    - numerical columns
    - categorical columns
    """
    df = _GLOBAL_CACHE.get('df')
    if df is None:
        return "No dataframe loaded. Use load_csv <path> first."
    
    numerical = df.select_dtypes(include=['number']).columns.tolist()
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()

    return (
        f"Numerical Columns: {numerical}\n"
        f"Categorical Columns: {categorical}"
    )


# -------------------------------------
# Simple global cache for the session
# -------------------------------------
_GLOBAL_CACHE = {}