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

        # pick model: prefer env override, else given arg, else default
        # self.model = (
        #     os.getenv("OPENAI_MODEL")
        #     or model
        #     or "gpt-4o-mini"
        # )
        self.model = model or "gpt-4o-mini"
        # self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        

    def generate(self, message: str) -> str:
        """
        Send a prompt to the LLM and return the response text (OpenAI v2 style)
        """
        resp = self.client.responses.create(
            model=self.model,
            input=message
        )
        # resp = self.client.chat.completions.create(
        #     mmodel=self.model,
        #     messages=[{"role": "user", "content": message}],
        #     temperature=0.2,
        # )
        # response = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": message}],
        #     temperature=0.2,
        # )

        # NOTE: v2 -> message is an object, not a dict

        return resp.output_text

        # return resp.choices[0].message.content

        # return response.choices[0].message["content"]
