"""
Full Agent class connecting planner, memory, executor
"""

from agent.core import AgentCore
from agent.planner import Planner
from agent.executor import Executor
from agent.tools import ToolRegistry
from agent.memory.module import MemoryModule # ✅ MEMORY

from tools import ml_tools
from tools.feature_tools import (
    split_data, encode_categoricals, scale_numericals, save_dataframe
)
from tools.file_tools import read_file, write_file
from tools.python_tools import run_python
from tools.project_tools import generate_scaffold
from tools.eda_tools import load_csv, preview_data, describe_data, column_info


class Agent:
    def __init__(self, model: str = None):
        # ✅ Memory Module
        self.memory = MemoryModule("agent_memory.db")

        # Core LLM
        self.core = AgentCore(model=model)

        # ✅ Pass memory into Planner
        self.planner = Planner(memory=self.memory)

        # Tools
        self.tools = ToolRegistry()
        self.tools.register("read_file", read_file)
        self.tools.register("write_file", write_file)
        self.tools.register("run_python", run_python)
        self.tools.register("generate_scaffold", generate_scaffold)
        self.tools.register("load_csv", load_csv)
        self.tools.register("preview_data", preview_data)
        self.tools.register("describe_data", describe_data)
        self.tools.register("column_info", column_info)
        self.tools.register("split_data", split_data)
        self.tools.register("encode_categoricals", encode_categoricals)
        self.tools.register("scale_numericals", scale_numericals)
        self.tools.register("save_dataframe", save_dataframe)
        self.tools.register("train_model", ml_tools.train_model)
        self.tools.register("evaluate_model", ml_tools.evaluate_model)
        self.tools.register("save_model", ml_tools.save_model)

        # ✅ Pass memory into Executor
        self.executor = Executor(self.core, self.tools, memory=self.memory)

    def run(self, user_input: str) -> str:
        # ✅ Step 1: Planner returns both plan + memory context
        plan_bundle = self.planner.create_plan(user_input)
        plan = plan_bundle["plan"]
        mem_ctx = plan_bundle["memory_context"]

        # ✅ Step 2: Give the LLM a chance to refine the plan using memory context
        # (This step is optional, but gives MUCH better multi-step clarity)
        planner_prompt = f"""
You are the Planner.
User goal: {user_input}

Relevant memory:
{mem_ctx}

Initial interpreted plan:
{plan}

Rewriete this into a clean, sequential, executable list of steps.
Keep steps simple and tool-focused.
"""
        refined_plan_text = self.core.generate(planner_prompt)

        # ✅ Optional: if your plan is already bucketed correctly, keep original tool steps.
        # For now, we keep your regex-based plan.

        # ✅ Step 3: Execute the steps
        return self.executor.execute_steps(plan)