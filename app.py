"""
FastAPI entrypoint for MLE-Agent
--------------------------------
Exposes endoints to interact with the agent or trigger ML operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from agent.agent import Agent
from tools import ml_tools
from tools.feature_tools import encode_categoricals, scale_numericals
import pandas as pd
import os
import uvicorn


# -----------------------------------------------------
# Initialize FastAPI app + agent
# -----------------------------------------------------
app = FastAPI(
    title="MLE-Agent API",
    version="1.0.0",
    description=(
        "A lightweight Machine Learning Engineering Assistant powered by FastAPI.\n\n"
        "It provides endpoints for:\n"
        "- Natural language ML planning (`/agent/query`)\n"
        "- Model training and prediction (`/ml/train`, `/ml/predict`)\n"
        "- Explainability and feature introspection (`/ml/features`, `/ml/explain`)\n\n"
        "Built by Kevin Woods."
    ),
    contact={
        "name": "Kevin Woods",
        "url": "https://github.com/woodskevinj",
        "email": "kevinwoods@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

bot = Agent() # initialize your agent once at startup

# -----------------------------------------------------
# Request models
# -----------------------------------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------------------------------
# Routes
# -----------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to MLE-Agent API 🚀"}


@app.post("/agent/query")
def run_agent(request: QueryRequest):
    """
    Accepts a natural-language query and returns the agent's response.
    """
    try:
        result = bot.run(request.query)
        return {"query": request.query, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# -----------------------------------------------------
# ML Training + Prediction Endpoints
# -----------------------------------------------------

# Shared state cache (same patteren as test scripts)
state = {}

@app.post("/ml/train")
async def train_model():
    """
    Train a model using the Telco dataset (for demo).
    """
    data_path = "data/telco/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    model_path = "models/churn_logreg.pkl"

    if not os.path.exists(data_path):
        return {"error": f"Dataset not found at {data_path}"}
    
    # --- Load and preprocess ---
    df = pd.read_csv(data_path)

    # Drop non-feature identifier columns
    df = df.drop(columns=["customerID"], errors="ignore")

    state["df"] = df
    
    encode_categoricals(state)
    scale_numericals(state)

    # --- Train and save model ---
    result = ml_tools.train_model(state, label="Churn", model_type="logistic")
    save_msg = ml_tools.save_model(state, path=model_path)

    return {
        "message": "Model training complete.",
        "details": result,
        "saved_to": model_path,
        "save_message": save_msg
    }


@app.post("/ml/predict")
async def predict(input_data: dict):
    """
    Predict churn for a single input sample.
    Expects JSON of feature:value pairs matching the trained model.
    """
    model_path = "models/churn_logreg.pkl"
    if not os.path.exists(model_path):
        return {"error": "Model not found.  Please train first using /ml/train."}
    
    model_bundle = ml_tools.joblib.load(model_path)
    model = model_bundle["model"]
    feature_names = model_bundle.get("feature_names", [])

    # Convert incoming JSON to DataFrame
    X_new = pd.DataFrame([input_data])

    # Align columns to match training
    for col in feature_names:
        if col not in X_new.columns:
            X_new[col] = 0

    X_new = X_new[feature_names]

    try:
        # Convert all data to numeric (handle accidental strings)
        X_new = X_new.apply(pd.to_numeric, errors="coerce").fillna(0)

        pred = model.predict(X_new)[0]
        proba = model.predict_proba(X_new)[0].tolist()
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}
    
    return {
        "prediction": int(pred), 
        "probabilities": proba,
        "features_used": list(X_new.columns)
        }


# ML Features
@app.get("/ml/features")
async def list_features():
    """
    Returns the feature names used during model training
    """
    model_path = "models/churn_logreg.pkl"
    if not os.path.exists(model_path):
        return {"error": "Model not found.  Train it first with /ml/train."}
    
    model_bundle = ml_tools.joblib.load(model_path)
    features = model_bundle.get("feature_names", [])
    return {"feature_names": features, "count": len(features)}




# -----------------------------------------------------
# Healthcheck Endpoint
# -----------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------------------------------
# Info Endpoint
# -----------------------------------------------------
@app.get("/info")
def info():
    return {
        "service": "MLE-Agent API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "core_modules": ["Planner", "Memory", "Executor", "ML Tools", "Explainability"],
        "model_bundle": {
            "type": "Logistic Regression",
            "explainability": "SHAP",
            "saved_model": "models/churn_logreg.pkl"
        },
        "description": (
            "MLE-Agent is a lightweight Machine Learning Engineering Assistant that "
            "combines natural language reasoning, feature engineering, model training, "
            " and explainability into one unified API."
        )
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MLE-Agent API",
        version="1.0.0",
        description=(
            "MLE-Agent is a lightweight Machine Learning Engineering Assistant that integrates "
            "planning, memory, ML tools, and explainability via FastAPI endpoints."
        ),
        routes=app.routes,
    )
    openapi_schema["info"]["x-service-metadata"] = {
        "servcie": "MLE-Agent",
        "model_type": "Logistic Regression + SHAP Explainability",
        "framework": "FastAPI",
        "author": "Kevin Woods",
        "github": "https://github.com/woodskevinj",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# -----------------------------------------------------
# To run: uvicorn app:app --reload
# -----------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)