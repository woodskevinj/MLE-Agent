"""
Run arbitrary Python code (use carefully)
"""

import io
import contextlib

def run_python(code: str) -> str:
    """
    Execute Python code and return stdout as a string.
    Does NOT allow variable leakage outside the function.
    """
    
    # Local namespace for isolation
    local_vars = {}

    # Capture stdout
    stdout_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout_buffer):
            exec(code, {}, local_vars)
    except Exception as e:
        return f"Error: {e}"
    
    return stdout_buffer.getvalue() if stdout_buffer.getvalue() else "Execution complete."