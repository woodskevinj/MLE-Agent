# 🤖 MLE-Agent

**MLE-Agent** is a lightweight Machine Learning Engineering Assistant that can:

- understand natural language requests
- decide which tools to use
- execute Python code safely
- read/write files
- generate ML project scaffolds
- and fall back to LLM responses when needed

This project demonstrates a real-world **agent architecture**:  
**Planner → Executor → Tools → LLM → Result**

It is designed to be modular, extensible, and easy to grow into a full ML engineering assistant.

---

## ✅ Current Capabilities

### 🔹 Natural Language Planning (Planner v3)

The agent converts plain English into a sequence of executable steps. Examples:

- “Read file notes.txt”
- “Run python: print(3\*7)”
- “Write this to file report.md: Hello!”
- “Create a new project called churn_model in projects”
- “Read file x, then run python y, then write result to z”
- “Explain this” → LLM fallback

The planner understands synonyms, handles uppercase/lowercase, and supports multi-step chained commands.

---

### 🔹 Implemented Tools

| Tool Name           | Description                                     |
| ------------------- | ----------------------------------------------- |
| `read_file`         | Read a text file from disk                      |
| `write_file`        | Write or overwrite a file                       |
| `run_python`        | Safely execute Python code (isolated namespace) |
| `generate_scaffold` | Create a project directory with starter files   |

More tools planned:

- EDA + ML model training helpers
- SHAP explainability modules
- Docker helpers
- Git + linting helpers
- AWS ECR/ECS deployment helpers

---

## ✅ Architecture Overview

User → Planner → Executor → Tools/LLM → Result

### **Planner (planner.py)**

- Rule-based intent detector
- Splits multi-step natural language commands
- Detects file actions, Python execution, scaffold generation
- Falls back to LLM when no tool matches

### **Executor (executor.py)**

- Executes each step sequentially
- Calls tools or LLM
- Passes outputs to the next step
- Supports optional DebugMode logging

### **Tools (tools/\*.py)**

Small, composable functions:

- File I/O
- Python execution
- Project generation

Tools can be added by simply registering them.

### **LLM Core (core.py)**

Uses OpenAI’s modern client:

```python
client.responses.create(model="gpt-4o-mini", input="...")
```

LLM is used only when:

- Planner detects "explain", "summarize", etc.

- No tool-based intent is found

### Debug Mode (debug.py)

```python
DEBUG = False
log("message")
```

## Central control for agent logging.

## ✅ Example Usage

### 1. Run the multi-step test

```bash
python -m scripts.test_multistep
```

Example output:

```arduino
USER: Read file demo.txt and then run python: print(2+2) and then write this to file result.txt: done
RESULT: File written: result.txt
```

### 2. Tool + LLM mixed output

```kotlin
USER: Run python: print(10*5) and then explain this
RESULT: The code prints 50...
```

### 3. Project generation

```sql
USER: Create a new project called fraud_model in .
RESULT: Project scaffold created at ./fraud_model
```

---

## ✅ Project Structure

```bash
MLE-Agent/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py              # main agent orchestrator
│   ├── core.py               # LLM wrapper (OpenAI API)
│   ├── planner.py            # Planner v3 (robust NL -> actions)
│   ├── executor.py           # Executor v2 (sequential execution)
│   ├── tools.py              # Tool registry
│   └── debug.py              # DEBUG toggle + log() helper
│
├── tools/
│   ├── __init__.py
│   ├── file_tools.py         # read_file, write_file
│   ├── python_tools.py       # run_python()
│   └── project_tools.py      # generate_scaffold()
│
├── api/
│   ├── __init__.py
│   └── main.py               # FastAPI endpoint (not implemented yet)
│
├── configs/
│   ├── agent_config.yaml     # future—config-driven behavior
│   ├── model_config.yaml
│   └── tools_config.yaml
│
├── data/
│   ├── telco/
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── README.md
│
├── notebooks/
│   ├── agent_walkthrough.ipynb
│   └── examples.ipynb
│
├── scripts/
│   ├── test_agent_local.py   # direct agent test
│   ├── test_python_tool.py   # python exec tool test
│   ├── test_multistep.py     # multistep chain test
│   ├── run_agent.py          # run agent from CLI
│   └── cli_demo.py           # interactive CLI
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

### Coming Next

⬜ ML/EDA tools

⬜ SHAP explainability

⬜ Dataset analysis

⬜ FastAPI agent endpoint (/agent/query)

⬜ Memory module (vector store)

⬜ Context history + tool reflection

⬜ Docker containerization

⬜ AWS ECR/ECS deploy option

---

## 🚀 Status

MLE-Agent is now a fully functional, modular agent framework with:

✅ Natural language intent detection

✅ Multi-step planning

✅ Tool routing

✅ Python execution

✅ File operations

✅ Project generation

✅ LLM fallback

✅ Clean architecture

This is a strong foundation for building a **real AI-powered ML engineering assistant**.

---

## 👨‍💻 Author

### Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
