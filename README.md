# 🤖 MLE-Agent

**MLE-Agent** is a lightweight Machine Learning Engineering Assistant that can:

- understand natural language requests
- decide which tools to use
- execute Python code safely
- read/write files
- generate ML project scaffolds
- and fall back to LLM responses when needed

This project demonstrates how to build a real agent architecture (Planner → Executor → Tools → LLM) step by step.

---

## ✅ Current Capabilities

### 🔹 Natural Language Planning (New!)

The agent can analyze your text and determine what action to take:

- “Read file notes.txt” → uses `read_file`
- “Write this to file x.py: …” → uses `write_file`
- “Run python: print(3\*7)” → uses `run_python`
- “Create a new project called fraud_model in ./projects” → uses `generate_scaffold`
- Anything else → LLM response via OpenAI

This is powered by a rule-based intent detector in `planner.py`.

---

### 🔹 Implemented Tools

| Tool Name           | Description                           |
| ------------------- | ------------------------------------- |
| `read_file`         | Read text files from disk             |
| `write_file`        | Create/overwrite files                |
| `run_python`        | Execute Python code in a sandbox      |
| `generate_scaffold` | Generate ML project folder structures |

More tools coming soon:

- ML/EDA tools
- SHAP explainability
- Docker tools
- Git helpers
- AWS ECR/ECS deployment helpers

---

## ✅ Architecture

**Planner → Executor → Tools → LLM → Result**

- **Planner**  
  Detects user intent using natural language  
  Creates a list of steps (`type="tool"` or `type="llm"`)

- **Executor**  
  Runs the steps in order  
  Calls tools or LLM depending on step type

- **Tools**  
  Reusable actions for Python execution, file IO, scaffold generation, etc.

- **LLM Core**  
  Uses OpenAI’s new Responses API (`client.responses.create`)

This architecture is modular, clean, and expandable.

---

## ✅ Example Usage

### 1. Run a natural language agent query

```bash
python -m scripts.test_planner
```

Produces results like:

```vbnet
USER: Read file test-output.txt
AGENT: Hello from MLE-Agent!

USER: Run python: print(3*7)
AGENT: 21

USER: Create a new project called churn_model in .
AGENT: Project scaffold created at: ./churn_model

```

LLM fallback example:

```vbnet
USER: What is cross validation?
AGENT: Cross-validation is a statistical technique used...

```

## ✅ Project Structure

```bash
MLE-Agent/
│
├── agent/
│   ├── core.py            # OpenAI interface (Responses API)
│   ├── planner.py         # Natural-language intent detection (v1)
│   ├── executor.py        # Executes tools & LLM calls
│   ├── memory.py          # Future: persistent agent memory
│   └── tools.py           # Tool registry
│
├── tools/
│   ├── file_tools.py      # read/write files
│   ├── python_tools.py    # run python safely
│   ├── project_tools.py   # scaffold generator
│   ├── ml_tools.py        # future ML/EDA utilities
│   ├── docker_tools.py    # future Docker helpers
│   ├── git_tools.py       # future Git helpers
│   └── aws_tools.py       # future AWS helpers
│
├── api/
│   └── main.py            # (soon) FastAPI interface
│
├── scripts/
│   ├── test_agent_local.py
│   ├── test_python_tool.py
│   ├── test_scaffold.py
│   └── test_planner.py
│
├── configs/
│   └── (YAML configuration files)
│
├── tests/
│   └── (unit tests)
│
├── data/
│   └── README.md
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

```

---

## ✅ Requirements

Make sure you have:

- Python 3.10+

- Virtual environment activated

- Install dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key (https://platform.openai.com/api-keys):

```arduino
export OPENAI_API_KEY="your-key"
```

## ✅ Roadmap

Next Steps (coming up next)

✅ Multi-step tool chaining

✅ More advanced planner logic

✅ EDA + ML training tools

✅ SHAP explainability

✅ FastAPI /agent/query endpoint

✅ Docker deployment

---

## 🚀 Status

MLE-Agent is now a functional, extensible agent framework with:

✅ Natural-language intent detection

✅ Tool routing

✅ Python execution

✅ File operations

✅ Project scaffold generation

✅ Full agent loop behavior

This is a professional-grade foundation for building a modern ML engineering assistant.

---

👨‍💻 Author

# Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
