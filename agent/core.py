"""
core.py — Core LLM interface and agent logic (first implementation).
"""

import os
from typing import Optional
from openai import OpenAI



class AgentCore:
    def __init__(self, model: Optional[str] = None):
        """
        Use env var OPEN_API_KEY. Do not pass api_key inline.
        """
        self.client = OpenAI()  # reads OPENAI_API_KEY from environment

        self.model = model or "gpt-4o-mini"
        

    def generate(self, message: str) -> str:
        """
        Send a prompt to the LLM and return the response text (OpenAI v2 style)
        """
        resp = self.client.responses.create(
            model=self.model,
            input=message
        )

        # NOTE: v2 -> message is an object, not a dict

        return resp.output_text
