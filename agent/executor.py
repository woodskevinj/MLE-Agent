"""
Executes planned steps using available tools
"""

# from agent.core import AgentCore
from agent.debug import log


class Executor:
    def __init__(self, core, tools, memory=None):
        self.core = core
        self.tools = tools
        self.memory = memory # ✅ MEMORY
        
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
                tool_name = step["name"]
                kwargs = step.get("kwargs", {})

                try:
                    result = self.tools.call(tool_name, **kwargs)
                    success = True
                    last_output = result
                except Exception as e:
                    result = str(e)
                    success = False
                    last_output = result

                # last_output = self.tools.call(step["name"], **step.get("kwargs", {}))
                log(f"[Executor] TOOL OUTPUT: {last_output}")

                # ✅ MEMORY: write episodic memory for tool execution
                if self.memory:
                    short_result = str(result)[:200]
                    self.memory.remember(
                        text=f"Ran tool '{tool_name}' with args={kwargs}. Result: {short_result}",
                        kind="episodic",
                        tags=["tool", tool_name],
                        importance=0.4 if success else 0.7,
                        summary=f"{tool_name} {'ok' if success else 'failed'}"
                    )

            elif stype == "llm":
                prompt = step["input"]
                if last_output:
                    prompt += f"\n\nPrevious result:\n{last_output}"

                result = self.core.generate(prompt)
                last_output = result

                # last_output = self.core.generate(prompt)
                log(f"[Executor] LLM OUTPUT: {last_output}")

                # ✅ MEMORY: store conversational / reasoning memory
                if self.memory:
                    short_result = str(result)[:200]
                    self.memory.remember(
                        text=f"LLM responded to prompt. Output: {short_result}",
                        kind="episodic",
                        tags=["llm"],
                        importance=0.3,
                        summary="LLM response"
                    )

            else:
                raise ValueError(f"Unknown step type: {stype}")
            
        return last_output
