"""
Executes planned steps using available tools
"""

# from agent.core import AgentCore
from agent.debug import log


class Executor:
    def __init__(self, core, tools):
        self.core = core
        self.tools = tools
        
    def execute_steps(self, steps):
        """
        Execute a list of steps in order
        """

        if isinstance(steps, dict):
            steps = [steps]

        last_output = None

        for step in steps:
            stype = step.get("type")
            log(f"[Executor] STEP: {step}")

            if stype == "tool":
                last_output = self.tools.call(step["name"], **step.get("kwargs", {}))
                log(f"[Executor] TOOL OUTPUT: {last_output}")

            elif stype == "llm":
                prompt = step["input"]
                if last_output:
                    prompt += f"\n\nPrevious result:\n{last_output}"
                last_output = self.core.generate(prompt)
                log(f"[Executor] LLM OUTPUT: {last_output}")

            else:
                raise ValueError(f"Unknown step type: {stype}")
            
        return last_output
