"""
Read/write tools for interacting with project files
"""

import os


def read_file(path: str) -> str:
    """
    Read text content from a file.
    Returns file content as a string
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, "r") as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """
    Write text content to a file.
    Overwrites if file exists.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(content)

    return f"File written: {path}"