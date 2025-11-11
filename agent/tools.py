"""
Tool registry and routing logic
"""

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.state= {} # shared memory for tools (df, splits, scaler, etc)

    def register(self, name: str, tool_fn):
        """
        Add a new tool function by name.
        """
        self.tools[name] = tool_fn

    def call(self, name: str, **kwargs):
        """
        Call a registered tool by name with keyword arguments.
        """
        tool_fn = self.tools.get(name)
        if tool_fn is None:
            raise ValueError(f"Tool '{name}' is not registered")
        
        return tool_fn(self.state, **kwargs)