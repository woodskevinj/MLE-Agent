from tools import ml_tools, feature_tools
import pandas as pd

state = {}

print("\n--- Load CSV ---")
state["df"] = pd.read_csv("data/telco/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("\n--- Encode Categoricals ---")
print(feature_tools.encode_categoricals(state))

print("\n--- Scale Numericals ---")
print(feature_tools.scale_numericals(state))

print("\n--- Train Model ---")
print(ml_tools.train_model(state, label="Churn", model_type="logistic"))

print("\n--- Save Model ---")
print(ml_tools.save_model(state, path="models/churn_logreg.pkl"))
