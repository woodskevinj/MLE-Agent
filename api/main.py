"""
FastAPI endpoint for interacting with MLE-Agent.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}