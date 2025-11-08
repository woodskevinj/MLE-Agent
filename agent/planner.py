"""
Plan generator for multi-step agent reasoning
"""

class Planner:
    def __init__(self):
        pass

    def create_plan(self, user_input: str):
        """
        Minimal plan: a single LLM step.
        """
        # steps = [
        #     {"action": "llm", "input": user_input},
        #     {"action": "respond", "input": "Return final answer to user"},
        # ]
        # return steps
        return [{"type": "llm", "input": user_input}]