"""
Short/long-term memory system for the agent.
"""

class Memory:
    def __init__(self):
        self.history = []

    def add(self, item):
        """
        Add a memory item to history
        """
        self.history.append(item)

    def retrieve(self, query: str):
        """
        Return full history for now.
        """
        return self.history