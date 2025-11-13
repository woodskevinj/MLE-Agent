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

## 🗂️ Project Structure

```bash
MLE-Agent/
│
├── agent/
│   ├── agent.py                 # Main agent orchestrator
│   ├── core.py                  # LLM wrapper (OpenAI SDK)
│   ├── planner.py               # Natural language planner (v3)
│   ├── executor.py              # Executes tools & LLM plans
│   ├── tools.py                 # Central tool registry
│   ├── debug.py                 # Debug mode + log helper
│   └── memory/                  # Memory subsystem
│       ├── module.py            # High-level memory interface
│       ├── store.py             # SQLite + FTS5 memory backend
│       ├── models.py            # Memory object schema
│       ├── ranking.py           # BM25 + recency + importance scoring
│       └── __init__.py
│
├── tools/
│   ├── file_tools.py            # File read/write helpers
│   ├── python_tools.py          # Safe Python execution
│   ├── project_tools.py         # Project scaffold generator
│   ├── eda_tools.py             # Data loading, preview, describe
│   ├── feature_tools.py         # Feature engineering utilities
│   └── ml_tools.py              # Model training & evaluation
│
├── scripts/
│   ├── test_agent_local.py      # Planner + Executor integration test
│   ├── test_multistep.py        # Multi-step natural language chain
│   ├── test_feature_tools.py    # Feature engineering test
│   ├── test_ml_tools.py         # ML training pipeline test
│   ├── test_memory_smoke.py     # Memory system smoke test
│   ├── run_agent.py             # CLI-based entry for agent
│   └── cli_demo.py              # Interactive terminal demo
│
├── tests/
│   ├── test_agent.py            # Unit tests for plan_


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
| Explainability      | SHAP and model insights             | 🔜     |
| FastAPI Endpoint    | `/agent/query` for API use          | 🔜     |
| Docker / ECS Deploy | Containerized endpoint              | 🔜     |

---

## 🚀 Status

MLE-Agent is now a memory-enabled ML assistant with:

✅ Natural language planning

✅ Memory-aware reasoning

✅ EDA + feature engineering

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
