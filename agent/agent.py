"""
Full Agent class connecting planner, memory, executor
"""

from agent.core import AgentCore
from agent.planner import Planner
from agent.memory import Memory
from agent.executor import Executor
from agent.tools import ToolRegistry


class Agent:
    def __init__(self, model: str = None):
        # Core LLM
        self.core = AgentCore(model=model)

        # Memory, planner, tools
        self.memory = Memory()
        self.planner = Planner()
        self.tool_registry = ToolRegistry()

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