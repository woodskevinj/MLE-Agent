"""
Tool registry and routing logic
"""

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool_fn):
        """
        Register a tool function.
        """
        self.tools[name] = tool_fn

    def call(self, name: str, **kwargs):
        tool_fn = self.tools.get(name)
        if tool_fn is None:
            raise ValueError(f"Tool '{name}' is not registered")
        return tool_fn(**kwargs)