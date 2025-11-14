"""
Test Script - Explainability Tools (SHAP)
-----------------------------------------
Runs a minimal explainability workflow:
1. Load dataframe
2. Train or load model
3. Compute SHAP values
4. Plot global and local explanations
"""


import joblib
from tools import eda_tools, feature_tools, ml_tools, explainability_tools

# shared session state
state = {}

print ("\n--- Load CSV ---")
print(eda_tools.load_csv(state, "data/telco/WA_Fn-UseC_-Telco-Customer-Churn.csv"))

print ("\n--- Encode Categoricals ---")
print(feature_tools.encode_categoricals(state))

print ("\n--- Scale Numericals ---")
print(feature_tools.scale_numericals(state))

print ("\n--- Train or Load Model ---")
try:
    # try loading pre-trained model if available
    model = joblib.load("models/churn_logreg.pkl")
    state["model"] = model
    print("Loaded existing model from models/churn_logreg.pkl")
except FileNotFoundError:
    print("No pre-trained model found - training new one...")
    print(ml_tools.train_model(state, label="Churn", model_type="logistic"))
    print(ml_tools.save_model(state, path="models/churn_logreg.pkl"))

print("\n--- Compute SHAP Values ---")
print(explainability_tools.compute_shap_values(state))

print("\n--- Plot Global Importance ---")
print(explainability_tools.plot_global_importance(state, top_n=10))

print("\n--- Plot Local Explanation ---")
print(explainability_tools.plot_local_explanation(state, row_index=0))

print("\n✅ Explainability test complete. Check 'images/' folder for plots.")

