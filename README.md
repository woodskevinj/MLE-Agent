# 🤖 MLE-Agent

**MLE-Agent** is a lightweight Machine Learning Engineering Assistant that can:

- understand natural language requests
- decide which tools to use
- execute Python code safely
- read/write files
- generate ML project scaffolds
- store and recall memory
- perform EDA and feature engineering
- train baseline ML models
- and fall back to LLM responses when needed

This project demonstrates a real-world **agent architecture**:  
**Planner → Memory → Executor → Tools/LLM → Result**

It is designed to be modular, extensible, and easy to grow into a full ML engineering assistant.

---

## ✅ Current Capabilities

### 🔹 Natural Language Planning (Planner v3)

The agent converts plain English into a sequence of executable steps:

- file read/write
- Python execution
- project scaffolding
- dataset loading and analysis
- model training
- LLM fallback

The planner understands synonyms, handles uppercase/lowercase, and supports multi-step chained commands.

### 🔹 Memory-Aware Planning (NEW)

MLE-Agent includes a full Memory Module with:

- **Episodic Memory** — stores tool calls, LLM responses, outcomes

- **Semantic Memory** — stores project facts, user preferences, and persistent knowledge

- **Automatic Recall** — powered by SQLite FTS5 + BM25 + recency + importance scoring

- **Planner context injection** - memory is automatically appended to the plan for richer context

Planner automatically receives:

- task-relevant memories

- recent session history

- pinned/important facts

Executor logs tool + LLM outcomes back to memory.

---

### 🔹 Implemented Tools

| Tool Name             | Description                                         |
| --------------------- | --------------------------------------------------- |
| `read_file`           | Read a text file from disk                          |
| `write_file`          | Write or overwrite a file                           |
| `run_python`          | Safely execute Python code                          |
| `generate_scaffold`   | Create starter ML project structures                |
| `load_csv`            | Load CSV datasets and preview structure             |
| `preview_data`        | Display top rows of the current dataset             |
| `describe_data`       | Show dataset statistics, missing values, and dtypes |
| `column_info`         | Display numerical vs categorical columns            |
| `encode_categoricals` | One-hot encode string columns for modeling          |
| `scale_numericals`    | Standardize numeric columns                         |
| `split_data`          | Split dataset into train/test sets                  |
| `train_model`         | Train logistic or random forest model               |
| `save_model`          | Persist trained models (auto-creates `/models`)     |

---

Planned future tools:

- ML model training helpers
- SHAP explainability modules
- Docker helpers
- AWS ECR/ECS deployment helpers

---

## ✅ Architecture Overview

**User → Planner → Memory Context → LLM (optional plan refinement) → Executor → Tools/LLM → Memory Logging → Result**

### 🧠 Planner (`planner.py`)

- Rule-based intent detector

- Splits multi-step natural language into structured actions

- Supports memory context injection before execution

### 🗂️ Memory Module (`agent/memory/*`)

- **store.py:** SQLite + FTS5 memory backend
- **module.py:** high-level API for remember(), recall(), context(), and recent()
- **ranking.py:** BM25 + recency + importance reranking

### ⚙️ Executor (`executor.py`)

- Executes tool or LLM steps
- Logs outcomes into episodic memory after every run

### 💬 LLM Core (`core.py`)

- Wrapper around OpenAI’s `client.responses.create()`
- Provides natural fallback answers for arbitrary questions

Uses OpenAI’s modern API:

```python
client.responses.create(model="gpt-4o-mini", input="...")
```

---

## 🧪 EDA + Feature Engineering Tools

**Located in:** `tools/eda_tools.py` and `tools/feature_tools.py`

| Function                | Description                               |
| ----------------------- | ----------------------------------------- |
| `load_csv(path)`        | Loads dataset into memory                 |
| `preview_data(n)`       | Shows first _n_ rows                      |
| `describe_data()`       | Summary stats + missing values + dtypes   |
| `column_info()`         | Lists numeric and categorical columns     |
| `encode_categoricals()` | One-hot encodes categorical columns       |
| `scale_numericals()`    | Standard-scales numeric features          |
| `split_data()`          | Splits dataset into training/testing sets |
| `save_dataframe(path)`  | Saves the transformed dataset to disk     |

These tools prepare your data for downstream modeling directly through the agent pipeline.

---

## 🤖 ML Training Tools

**Located in:** `tools/ml_tools.py`

| Function                                                   | Description                                        |
| ---------------------------------------------------------- | -------------------------------------------------- |
| `train_model(state, label="Churn", model_type="logistic")` | Trains logistic regression or random forest models |
| `evaluate_model(state, path=None)`                         | Evaluates a cached or saved model                  |
| `save_model(state, path="models/model.pkl")`               | Saves trained model to the `/models` folder        |

**Example Run**

```bash
python -m scripts.test_ml_tools
```

Output:

```bash
Model trained successfully (logistic).
Accuracy: 0.8084
Confusion Matrix:
[[958  78]
 [192 181]]
Classification Report:
...
Model saved to models/churn_logreg.pkl
```

---

## ✅ Memory Example

```bash
USER: Run python: print(5*5)

USER: What did I run earlier?
RESULT: Based on memory: You ran print(5*5) and the output was 25.
```

---

## ✅ Data + Feature Example

```bash
USER: load csv file data/telco/WA_Fn-UseC_-Telco-Customer-Churn.csv
USER: encode categoricals
USER: scale numericals
USER: split data
USER: save dataframe to data/telco/transformed.csv
```

---

## 🧠 Model Explainability (SHAP)

The **Explainability Module** helps interpret trained models by showing which features most influence predictions — both globally (across all customers) and locally (for individual predictions).

### 🔹 Capabilities

- **Global Feature Importance**

  - Uses SHAP to compute average absolute impact of each feature.

  - Saves visual plot: images/shap_global.png

  - Helps understand which customer attributes drive churn overall.

- **Local Explanation**

  - Visualizes one sample’s prediction reason using a SHAP waterfall plot.

  - Saves visual plot: images/shap_local.png

  - Shows why a specific customer is predicted to churn or stay.

### 🔹 Example Workflow

```bash# Run explainability workflow
python -m scripts.test_explainability_tools
```

Expected Output:

```pgsql
--- Load CSV ---
CSV loaded successfully. Shape: (7043, 21)
--- Encode Categoricals ---
Categoricals encoded. New shape: (7043, 32)
--- Scale Numericals ---
Numerical features scaled (3 columns).
--- Train or Load Model ---
Loaded existing model from models/churn_logreg.pkl
--- Compute SHAP Values ---
SHAP values computed for 7043 samples and 31 features.
--- Plot Global Importance ---
Global SHAP importance plot saved to images/shap_global.png
--- Plot Local Explanation ---
Local SHAP explanation saved to images/shap_local.png
✅ Explainability test complete. Check 'images/' folder for plots.
```

### 🔹 Example Outputs

| Plot                                   | Description                       |
| -------------------------------------- | --------------------------------- |
| ![Global SHAP](images/shap_global.png) | Top global feature importances    |
| ![Local SHAP](images/shap_local.png)   | Single-customer local explanation |

---

## ⚡ FastAPI Integration (MLE-Agent API)

MLE-Agent now runs as a **RESTful service** powered by **FastAPI**, exposing endpoints for both agent queries and ML model operations.

### 🔹 Endpoints Overview

| **Endpoint** | **Method** | **Description**                                      |
| ------------ | ---------- | ---------------------------------------------------- |
| /            | GET        | Root health message                                  |
| /health      | GET        | Service health check                                 |
| /info        | GET        | Returns metadata about the API and model             |
| /agent/query | POST       | Sends a natural-language request to the MLE-Agent    |
| /ml/train    | POST       | Trains a churn prediction model on the Telco dataset |
| /ml/predict  | POST       | Makes a churn prediction for a new input sample      |
| /ml/features | GET        | Returns all feature names used by the trained model  |

### 🔹 Example Requests

1️⃣ **Agent Query**

```bash
curl -X POST "http://127.0.0.1:8000/agent/query" \
 -H "Content-Type: application/json" \
 -d '{"query": "What is logistic regression?"}'
```

**Response**:

```json
{
  "query": "What is logistic regression?",
  "response": "Logistic regression is a statistical method used for binary classification..."
}
```

2️⃣ **Train Model**

```bash
curl -X POST "http://127.0.0.1:8000/ml/train"
```

**Response**:

```json
{
  "message": "Model training complete.",
  "details": "Model trained successfully (logistic). Accuracy: 0.8084",
  "saved_to": "models/churn_logreg.pkl"
}
```

3️⃣ **Predict Churn**

```bash
curl -X POST "http://127.0.0.1:8000/ml/predict" \
 -H "Content-Type: application/json" \
 -d '{
"tenure": 12,
"MonthlyCharges": 70.35,
"TotalCharges": 845.5,
"gender_Male": 1,
"SeniorCitizen": 0,
"Partner_Yes": 1,
"Dependents_Yes": 0,
"InternetService_Fiber optic": 1,
"Contract_Two year": 0
}'
```

**Response**:

```json
{
"prediction": 1,
"probabilities": [0.000000001, 0.999999999],
"features_used": ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges", ...]
}
```

4️⃣ **Feature List**

```bash
curl -X GET "http://127.0.0.1:8000/ml/features"
```

**Response**:

```json
{
"feature_names": ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges", ...],
"count": 30
}
```

🔹 **Swagger UI**

FastAPI auto-generates interactive API docs at:

- Swagger: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

🔹 **Run Locally**

```bash
uvicorn app:app --reload
```

---

## 🗂️ Project Structure

```bash
MLE-Agent/
│
├── agent/
│   ├── agent.py
│   ├── core.py
│   ├── planner.py
│   ├── executor.py
│   ├── tools.py
│   ├── debug.py
│   └── memory/
│       ├── module.py
│       ├── store.py
│       ├── models.py
│       ├── ranking.py
│       └── __init__.py
│
├── tools/
│   ├── file_tools.py
│   ├── python_tools.py
│   ├── project_tools.py
│   ├── eda_tools.py
│   ├── feature_tools.py
│   ├── ml_tools.py
│   └── explainability_tools.py
│
├── scripts/
│   ├── test_agent_local.py
│   ├── test_multistep.py
│   ├── test_feature_tools.py
│   ├── test_ml_tools.py
│   ├── test_explainability_tools.py
│   ├── run_agent.py
│   └── cli_demo.py
│
├── models/
│   └── churn_logreg.pkl
│
├── images/
│   ├── shap_global.png
│   └── shap_local.png
│
├── data/
│   └── telco/WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_end_to_end.py
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

```

---

## ✅ Requirements

Make sure you have:

1. Python 3.10+

2. Virtual environment activated

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key (https://platform.openai.com/api-keys):

```bash
export OPENAI_API_KEY="your-key"
```

---

## ✅ Roadmap

| Stage               | Description                         | Status |
| ------------------- | ----------------------------------- | ------ |
| Planner v3          | Multi-step natural language planner | ✅     |
| Memory Module       | Episodic + semantic recall          | ✅     |
| EDA Tools           | Dataset loading and exploration     | ✅     |
| Feature Tools       | Encoding, scaling, splitting        | ✅     |
| ML Tools            | Model training and saving           | ✅     |
| Explainability      | SHAP and model insights             | ✅     |
| FastAPI Endpoint    | `/agent/query` for API use          | ✅     |
| Docker / ECS Deploy | Containerized endpoint              | 🔜     |

---

## 🚀 Status

MLE-Agent is now a memory-enabled ML assistant with:

✅ Natural language planning

✅ Memory-aware reasoning

✅ EDA + feature engineering

✅ Explainability

✅ Model training + saving

✅ Clean modular design

A strong foundation for building a true Applied ML Engineering Agent.

---

## 👨‍💻 Author

### Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
