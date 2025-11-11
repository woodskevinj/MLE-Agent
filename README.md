# 🤖 MLE-Agent

**MLE-Agent** is a lightweight Machine Learning Engineering Assistant that can:

- understand natural language requests
- decide which tools to use
- execute Python code safely
- read/write files
- generate ML project scaffolds
- store and recall memory
- and fall back to LLM responses when needed

This project demonstrates a real-world **agent architecture**:  
**Planner → Memory → Executor → Tools/LLM → Result**

It is designed to be modular, extensible, and easy to grow into a full ML engineering assistant.

---

## ✅ Current Capabilities

### 🔹 Natural Language Planning (Planner v3)

The agent converts plain English into a sequence of executable steps. Examples:

- file read/write

- Python execution

- Project scaffolding

- LLM fallback

The planner understands synonyms, handles uppercase/lowercase, and supports multi-step chained commands.

### 🔹 Memory-Aware Planning (NEW)

MLE-Agent now includes a full Memory Module with:

- **Episodic Memory**:

  Stores tool calls, LLM responses, errors, outcomes.

- **Semantic Memory**:

  Stores long-lived knowledge like project details, user preferences, or environment rules.

- **Automatic recall**:

  Memory is retrieved via SQLite FTS5 (BM25 ranking) + recency + importance scoring.

- **Planner Context Injection**:
  When the user issues a new request, Planner automatically receives a memory_context block containing:

  - task-relevant memories

  - recent agent history

  - pinned or high-importance facts

This makes the agent more stable across sessions and more capable of multi-step reasoning.

---

### 🔹 Implemented Tools

| Tool Name           | Description                                     |
| ------------------- | ----------------------------------------------- |
| `read_file`         | Read a text file from disk                      |
| `write_file`        | Write or overwrite a file                       |
| `run_python`        | Safely execute Python code (isolated namespace) |
| `generate_scaffold` | Create starter ML project structures            |

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

### **Memory Module (agent/memory/\*)**

- store.py: SQLite FTS5 memory backend

- models.py: Memory objects (episodic, semantic)

- ranking.py: BM25 + recency + importance reranking

- module.py: High-level memory API:

  - remember()

  - recall()

  - context()

  - recent()

Planner uses memory.context() before forming a plan.

Executor logs all outcomes back into memory.

### **Executor (executor.py)**

- Executes tool actions or LLM responses

- Feeds results into the next step

- Logs episodic memories after every tool or LLM output

### **LLM Core (core.py)**

Simple interface around OpenAI’s SDK using:

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
│   └── project_tools.py
│
├── scripts/
│   ├── test_agent_local.py
│   ├── test_multistep.py
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

✅ Multi-step tool chaining

✅ Planner v3 (synonyms, case-insensitive, code-preserving)

✅ Executor v2

✅ Python + file I/O tools

✅ Project scaffold tool

✅ Memory Module (episodic + semantic)

✅ Memory-aware planning & recall

### Coming Next

⬜ ML/EDA tools

⬜ SHAP explainability

⬜ Dataset analysis

⬜ FastAPI agent endpoint (/agent/query)

⬜ Vector search memory (embeddings)

⬜ Tool self-reflection

⬜ Docker containerization

⬜ AWS ECR/ECS agent deploy option

---

## 🚀 Status

MLE-Agent is now a memory-enabled agent framework with:

✅ Natural language intent detection

✅ Multi-step planning

✅ Memory-aware context

✅ Tool routing

✅ Python execution

✅ File operations

✅ Project generation

✅ LLM fallback

✅ Clean architecture

A strong foundation for building a **true ML engineering assistant**.

---

## 👨‍💻 Author

### Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
