"""
Executes planned steps using available tools
"""

from agent.core import AgentCore


class Executor:
    def __init__(self, tools=None):
        # tools can be a ToolRegistry or a plain dict {name: fn}
        self.core = AgentCore()
        self.tools = tools or {}
        
        
        
    def execute_steps(self, step: dict):
        """
        Executes a single planning step.
        Expected shape (MVP):
            {"type": "llm", "input": "some prompt"}
            or {"type": "tool", "name": "read_file", "kwargs": {...}}
        """
        step_type = step.get("type")

        # LLM call
        if step_type == "llm":
            return self.core.generate(step["input"])
        
        # Tool call
        if step_type == "tool":
            name = step["name"]
            kwargs = step.get("kwargs", {})
            return self.tools.call(name, **kwargs)
            # ToolRegistry has .call; plain dict has callable values
            #if hasattr(self.tools, "call"):
                # return self.tools.call(name, **kwargs)
            # tool_fn = self.tools.get(name)
            # if tool_fn is None:
            #     raise ValueError(f"Tool '{name}' not registered")
            # return tool_fn(**kwargs)
        
        raise ValueError(f"Unknown step type: {step_type}")

        # action = step.get("action")

        # if action == "llm":
        #     # call the llm with the given input
        #     return self.core.generate(step["input"])
        
        # if action == "respond":
        #     return step["input"]
        
        # #unknown action
        # return f"Unknown action: {action}"
