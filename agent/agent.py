"""
Full Agent class connecting planner, memory, executor
"""

from agent.core import AgentCore
from agent.planner import Planner
from agent.memory import Memory
from agent.executor import Executor
from agent.tools import ToolRegistry
from tools.file_tools import read_file, write_file
from tools.python_tools import run_python
from tools.project_tools import generate_scaffold


class Agent:
    def __init__(self, model: str = None):
        # Core LLM
        self.core = AgentCore(model=model)

        # Memory, planner, tools
        self.memory = Memory()
        self.planner = Planner()
        self.tool_registry = ToolRegistry()

        # Register base tools
        self.tool_registry.register("read_file", read_file)
        self.tool_registry.register("write_file", write_file)
        self.tool_registry.register("run_python", run_python)
        self.tool_registry.register("generate_scaffold", generate_scaffold)

        # IMPORTANT: pass a tools registry/dict into Executor to avoid the
        # "missing positional argument: 'tools'" error seen
        self.executor = Executor(tools=self.tool_registry)

    def run(self, user_input: str):
        """
        Main entry point:
        - creates a plan
        - executes each step
        - stores memory
        - returns last result
        """
        plan = self.planner.create_plan(user_input)

        result = None
        for step in plan:
            result = self.executor.execute_steps(step)
            #self.memory.add(f"Executed step: {step}")

        return result