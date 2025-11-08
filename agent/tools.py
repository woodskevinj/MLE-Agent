"""
Tool registry and routing logic
"""

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool_fn):
        """
        Add a new tool function by name.
        """
        self.tools[name] = tool_fn

    def call(self, name: str, **kwargs):
        """
        Call a registered tool by name with keyword arguments.
        """
        # tool_fn = self.tools.get(name)
        # if tool_fn is None:
        #     raise ValueError(f"Tool '{name}' is not registered")
        # return tool_fn(**kwargs)
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered.")
        return self.tools[name](**kwargs)