"""
Full Agent class connecting planner, memory, executor
"""

from agent.core import AgentCore
from agent.planner import Planner
from agent.executor import Executor
from agent.tools import ToolRegistry
from tools.file_tools import read_file, write_file
from tools.python_tools import run_python
from tools.project_tools import generate_scaffold


class Agent:
    def __init__(self, model: str = None):
        # Core LLM
        self.core = AgentCore()
        self.planner = Planner()
        self.tools = ToolRegistry()

        # Register tools
        self.tools.register("read_file", read_file)
        self.tools.register("write_file", write_file)
        self.tools.register("run_python", run_python)
        self.tools.register("generate_scaffold", generate_scaffold)

        self.executor = Executor(self.core, self.tools)

    def run(self, user_input: str) -> str:
        plan = self.planner.create_plan(user_input)
        return self.executor.execute_steps(plan)