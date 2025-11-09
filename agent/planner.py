"""
Plan generator for multi-step agent reasoning
"""

import re


class Planner:
    def __init__(self):
        pass

    def create_plan(self, user_input: str):
        """
        Natural language planning logic (v1).
        Detects whethere the user wants to:
        - read a file
        - write a file
        - run python
        - generate a scaffold
        Otherwise -> normal LLM response.
        """

        text = user_input.lower()

        # ---------------------------
        # 1. Detect: READ FILE
        # ---------------------------
        match = re.search(r"(read|open)\s+(?:the\s+)?file\s+([^\s]+)", text)
        if match:
            path = match.group(2)
            return [
                {"type": "tool", "name": "read_file", "kwargs": {"path": path}}
            ]
        
        # ---------------------------
        # 2. Detect: WRITE FILE
        # ---------------------------
        # Example:
        # "Write this to file test.txt: Hello World"
        match = re.search(r"write (?:this )?to file ([^\s:]+):\s*(.*)", text)
        if match:
            path = match.group(1)
            content = match.group(2)
            return [
                {"type": "tool", "name": "write_file", "kwargs": {"path": path, "content": content}}
            ]
        
        # ---------------------------
        # 3. Detect: RUN PYTHON
        # ---------------------------
        # Example:
        # "run python: print(5+5)"
        match = re.search(r"run python:?(.+)", text, re.DOTALL)
        if match:
            code = match.group(1).strip()
            return [
                {"type": "tool", "name": "run_python", "kwargs": {"code": code}}
            ]
        
        # ---------------------------
        # 4. Detect: GENERAT SCAFFOLD
        # ---------------------------
        # Example:
        # "create a new project called churn inside projects"
        match = re.search(r"create (?:a )?(?:new )?project called ([^\s]+) in ([^\s]+)", text)
        if match:
            project_name = match.group(1)
            base_path = match.group(2)
            return [
                {
                    "type": "tool",
                    "name": "generate_scaffold",
                    "kwargs": {
                        "base_path": base_path,
                        "project_name": project_name
                    }
                }
            ]
        
        # ---------------------------
        # Default: Just respond normally
        # ---------------------------
        return [
            {"type": "llm", "input": user_input}
        ]