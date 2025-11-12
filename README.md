# 🤖 MLE-Agent

**MLE-Agent** is a lightweight Machine Learning Engineering Assistant that can:

- understand natural language requests
- decide which tools to use
- execute Python code safely
- read/write files
- generate ML project scaffolds
- store and recall memory
- perform EDA and feature engineering
- and fall back to LLM responses when needed

This project demonstrates a real-world **agent architecture**:  
**Planner → Memory → Executor → Tools/LLM → Result**

It is designed to be modular, extensible, and easy to grow into a full ML engineering assistant.

---

## ✅ Current Capabilities

### 🔹 Natural Language Planning (Planner v3)

The agent converts plain English into a sequence of executable steps:

- read/write files

- run Python

- generate project scaffolds

- load CSV data

- preview or summarize data

- feature engineering steps

- and fallback to LLM when needed

The planner understands synonyms, handles uppercase/lowercase, and supports multi-step chained commands.

### 🔹 Memory-Aware Planning (NEW)

MLE-Agent includes a full Memory Module with:

- **Episodic Memory** (tool calls, outcomes, LLM results)

- **Semantic Memory** (long-lived facts, preferences, project info)

- **Fast Recall** via SQLite FTS5 + BM25 + recency scoring

- **Automatic context injection** into Planner to improve reasoning

Planner automatically receives:

- task-relevant memories

- recent session history

- pinned/important facts

Executor logs tool + LLM outcomes back to memory.

---

### 🔹 Implemented Tools

| Tool Name           | Description                                     |
| ------------------- | ----------------------------------------------- |
| `read_file`         | Read a text file from disk                      |
| `write_file`        | Write or overwrite a file                       |
| `run_python`        | Safely execute Python code (isolated namespace) |
| `generate_scaffold` | Create starter ML project structures            |
| load_csv            | Load a CSV dataset into agent state             |
| preview_data        | Show first N rows of loaded dataset             |
| describe_data       | Full dataset summary (stats, types, missing)    |
| column_info         | List numerical and categorical columns          |
| encode_categoricals | One-hot encode categorical features             |
| scale_numericals    | Scale numerical features                        |
| split_data          | Train/test split of dataset                     |
| save_dataframe      | Save transformed data                           |

All EDA + feature tools operate on a shared tool state, so each step can depend on the previous one (like a real ML pipeline).

---

Planned future tools:

- EDA utilitites
- ML model training helpers
- SHAP explainability modules
- Docker helpers
- AWS ECR/ECS deployment helpers

---

## ✅ Architecture Overview

User → Planner → **Memory Context** → LLM (optional plan refinement) → Executor → Tools/LLM → **Memory Logging** → Result

### **Planner (planner.py)**

- Rule-based intent detector

- Splits multi-step language into structured actions

- Detects known tool actions

- Falls back to LLM when no pattern matches

- Now includes memory_context for richer planning

### **Memory System (agent/memory/\*)**

- SQLite FTS5 store

- BM25 ranking

- Episodic + semantic memory

- recall(), remember(), context(), recent()

### **Tools System (agent/tools.py)**

- Shared state dict across all tools

- Allows sequential data operations

- Used by EDA + feature engineering tools

### **Executor (executor.py)**

- Runs each planned step

- Handles tool routing or LLM calls

- Logs all results to memory

### **LLM Core (core.py)**

Uses OpenAI’s modern API:

```python
client.responses.create(model="gpt-4o-mini", input="...")
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

## ✅ Project Structure

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
│   └── feature_tools.py
│
├── scripts/
│   ├── test_agent_local.py
│   ├── test_multistep.py
│   ├── test_feature_tools.py
│   ├── run_agent.py
│   └── cli_demo.py
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

### Next Steps (coming up next)

✅ Multi-step planning

✅ Memory module (episodic + semantic)

✅ Memory-aware planning

✅ Project scaffold tool

✅ Full EDA tool suite

✅ Feature engineering tools

### Coming Next

⬜ ML training tools (LogReg, RF, XGBoost)

⬜ Model evaluation tools

⬜ SHAP explainability

⬜ FastAPI agent endpoint (/agent/query)

⬜ Vector search memory (embeddings)

⬜ Agent self-reflection

⬜ Docker containerization

⬜ AWS ECR/ECS agent deploy option

---

## 🚀 Status

MLE-Agent is now a memory-enabled, stateful ML assistant with:

✅ Natural language tool execution

✅ Multi-step planning

✅ EDA + Feature Engineering

✅ Project generation

✅ Memory recall

✅ LLM fallback

✅ Clean modular architecture

---

## 👨‍💻 Author

### Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
