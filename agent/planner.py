"""
Natural language multi-step planning (v2)
"""

import re
from agent.debug import log


class Planner:
    def __init__(self, memory=None):
        # Add memory moduel if avail
        self.memory = memory

        # Natural language sequence markers (case-insensitive)
        self.splitter_pattern = r"(?i)\b(?:and then|then|next|after that|followed by|and)\b"
        

    def _split_into_steps(self, text: str):
        """
        Split natural language into sequential clauses.
        Preserves original casing
        """
        raw_parts = re.split(self.splitter_pattern, text)
        clauses = [p.strip() for p in raw_parts if p.strip()]
        log(f"[Planner] Clauses: {clauses}")
        return clauses
    
    def _detect_single_intent(self, clause: str):
        """
        Detect a single action (tool or LLM fallback).
        Uses clause_lower for intent, clause for exact extraction.
        """
        clause_lower = clause.lower()

        # ---------------------------
        # READ FILE INTENT
        # ---------------------------
        read_patterns = [
            r"(read|open|load|show|display)\s+(?:the\s+)?file\s+([^\s]+)"
        ]
        for pat in read_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {"type": "tool", 
                        "name": "read_file",
                        "kwargs": {"path": m.group(2)}}
        
        # ---------------------------
        # WRITE FILE INTENT
        # ---------------------------
        write_patterns = [
            r"(write|save|create|output)\s+(?:this\s+)?to\s+file\s+([^\s:]+):\s*(.+)"
        ]
        for pat in write_patterns:
            m = re.search(pat, clause_lower, re.DOTALL)
            if m:
                # Extract exact content using original clause
                orig = re.search(pat, clause, re.DOTALL)
                return {
                    "type": "tool", 
                    "name": "write_file",
                    "kwargs": {
                        "path": orig.group(2), 
                        "content": orig.group(3)
                    }
                }
        
        # ---------------------------
        # RUN PYTHON
        # ---------------------------
        python_patterns = [
            r"(run python|execute python|run code|python code|execute code)[: ]+(.+)"
        ]
        for pat in python_patterns:
            m = re.search(pat, clause_lower, re.DOTALL)
            if m:
                # Extract code from original clause (preserves exact casing)
                orig = re.search(pat, clause, re.IGNORECASE | re.DOTALL)
                if orig:
                    code = orig.group(2).strip()
                    return {
                        "type": "tool", 
                        "name": "run_python",
                        "kwargs": {"code": code}
                    }
        
        # ---------------------------
        # GENERATE SCAFFOLD
        # ---------------------------
        scaffold_patterns = [
            r"(create|make|generate)\s+(?:a\s+)?project\s+(?:called|named)\s+([^\s]+)\s+in\s+([^\s]+)"
        ]

        for pat in scaffold_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool", 
                    "name": "generate_scaffold",
                    "kwargs": {
                        "project_name": m.group(2),
                        "base_path": m.group(3)
                    }
                }
            
        # LOAD CSV
        csv_patterns = [
            r"(load|read)\s+(?:the\s+)?csv\s+file\s+([^\s]+)",
            r"(load|read)\s+([^\s]+\.csv)"
        ]
        for pat in csv_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "load_csv",
                    "kwargs": {"path": m.group(2)}
                }
            
        # PREVIEW DATA
        preview_patterns = [
            r"(show|preview|display)\s+(?:the\s+)?data(?:\s+head)?",
            r"(show|preview)\s+first\s+(\d+)\s+rows"
        ]
        for pat in preview_patterns:
            m = re.search(pat, clause_lower)
            if m:
                n = 5
                if len(m.groups()) >= 2 and m.group(2).isdigit():
                    n = int(m.group(2))
                return {
                    "type": "tool",
                    "name": "preview_data",
                    "kwargs": {"n": n}
                }
            
        # DESCRIBE DATA
        describe_patterns = [
            r"(describe|summarize)\s+(?:the\s+)?data",
            r"data\s+summary"
        ]
        for pat in describe_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "describe_data",
                    "kwargs": {}
                }
            
        # COLUMN INFO
        colinfo_patterns = [
            r"(show|list)\s+(?:the\s+)?columns",
            r"(column|columns)\s+info"
        ]

        for pat in colinfo_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "column_info",
                    "kwargs": {}
                }
            
        # TRAIN/TEST SPLIT
        split_patterns = [
            r"(split|train test split|train\/test)\s+data",
            r"split\s+the\s+data"
        ]
        for pat in split_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "split_data",
                    "kwargs": {}
                }
            
        encode_patterns = [
            r"(encode|transform)\s+(categorical|categoricals|categories)",
            r"encode\s+categoricals"
        ]
        for pat in encode_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "encode_categoricals",
                    "kwargs": {}
                }
            
        scale_patterns = [
            r"(scale|standardize|normalize)\s+(numerical|numeric|numbers)",
            r"scale\s+numerical"
        ]
        for pat in scale_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "scale_numericals",
                    "kwargs": {}
                }
            
        save_patterns = [
            r"(save|export)\s+(?:the\s+)?dataframe\s+to\s+([^\s]+)",
        ]
        for pat in save_patterns:
            m = re.search(pat, clause_lower)
            if m:
                return {
                    "type": "tool",
                    "name": "save_dataframe",
                    "kwargs": {"path": m.group(2)}
                }
        
        # ---------------------------
        # DEFAULT -> LLM
        # ---------------------------
        return {"type": "llm", "input": clause}

    def create_plan(self, user_input: str):
        """
        Multi-step NL -> full sequential tool plan
        """
        clauses = self._split_into_steps(user_input)
        plan = [self._detect_single_intent(c) for c in clauses]

        # Fallback
        if not plan:
            return [{"type": "llm", "input": user_input}]
        
        # log(f"[Planner] Final plan: {plan}")
        # return plan
        log(f"[Planner] Final plan (before memory): {plan}")

        # =====================================================
        # ✅ MEMORY CONTEXT
        # =====================================================
        mem_ctx = ""
        if self.memory:
            mem_ctx = self.memory.context(task=user_input, token_budget_chars=2400)

        return {
            "plan": plan,
            "memory_context": mem_ctx
        }

    
