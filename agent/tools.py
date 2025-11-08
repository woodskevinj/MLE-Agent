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
        """
        Call a registered tool by name.
        """
        pass