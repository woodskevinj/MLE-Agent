# 🤖 MLE-Agent

A lightweight **Machine Learning Engineering Assistant** designed to help you rapidly build ML projects, run code, analyze datasets, create files, and scaffold full project structures.

This project is built step-by-step, demonstrating how to construct a real LLM-powered agent system with tools, planning, and execution.

---

## ✅ Current Capabilities

MLE-Agent currently supports:

### ✅ Core LLM Engine

- Uses OpenAI’s latest **Responses API**
- Model: **gpt-4o-mini** (configurable)
- Clean, modular Core class for generation

### ✅ Working Agent Loop

- Planner → creates step list
- Executor → runs LLM or tools
- Memory (stubbed, ready for future expansion)

### ✅ Implemented Tools

Right now, MLE-Agent can:

✅ **read files**  
✅ **write files**  
✅ **execute Python code** (sandboxed)  
✅ **generate project scaffolds** (folders + README)

This makes it capable of:

- running pandas code
- manipulating data
- generating starter ML project layouts
- preparing notebooks, scripts, and pipelines
- reading/writing intermediate data or configs

And we’ll expand more tool categories soon (Docker, Git, AWS, ML training, etc.)

---

## ✅ Example Usage (Local Test)

### Run a simple agent query:

```bash
python -m scripts.test_agent_local
```

You’ll see a real LLM response from the agent:

```css
A decision tree is a flowchart-like model...
```

Run Python execution:

```bash
python -m scripts.test_python_tool
```

Generate a project scaffold:

```bash
python -m scripts.test_scaffold
```

---

## ✅ Project Structure

```bash
MLE-Agent/
│
├── agent/
│   ├── __init__.py
│   ├── core.py                # LLM interface (OpenAI Responses API)
│   ├── planner.py             # generates multi-step plans
│   ├── memory.py              # vector + short-term memory (future)
│   ├── executor.py            # executes steps + tool calls
│   └── tools.py               # tool registry & dispatch system
│
├── tools/
│   ├── __init__.py
│   ├── file_tools.py          # read/write files
│   ├── python_tools.py        # execute python safely
│   ├── project_tools.py       # project scaffold generator
│   ├── ml_tools.py            # (future) EDA, training, SHAP
│   ├── docker_tools.py        # (future) Docker helpers
│   ├── git_tools.py           # (future) Git commit helpers
│   └── aws_tools.py           # (future) AWS templates / ECR/ECS
│
├── api/
│   ├── __init__.py
│   └── main.py                # (soon) FastAPI interface
│
├── configs/
│   ├── agent_config.yaml
│   ├── model_config.yaml
│   └── tools_config.yaml
│
├── data/
│   └── README.md
│
├── notebooks/
│   ├── agent_walkthrough.ipynb
│   └── examples.ipynb
│
├── scripts/
│   ├── test_agent_local.py
│   ├── test_python_tool.py
│   ├── test_scaffold.py
│   └── run_agent.py
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

✅ Add real planning logic

- agent decides when to use LLM vs tools
- multi-step workflows
- tool-chaining

Future Milestones

✅ EDA tools

✅ Model training tool

✅ SHAP explainability

✅ FastAPI endpoint /agent/query

✅ Docker deployment

✅ Git integration

✅ AWS (ECR/ECS) helpers

---

## 🚀 Status

MLE-Agent is now an actively working prototype with:

- a functioning agent loop

- OpenAI integration

- tool execution

- Python sandbox

- file operations

- full scaffold generator

This is now a professional-grade starting point for building a real ML engineering assistant.

---

👨‍💻 Author

# Kevin Woods

Applied ML Engineer

AWS Certified AI Practitioner

AWS Machine Learning Certified Engineer – Associate

- 🔗 [GitHub: woodskevinj](https://github.com/woodskevinj)
