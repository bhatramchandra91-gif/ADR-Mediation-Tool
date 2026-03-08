from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key="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"
)

MODEL = "gpt-4o-mini"

MAX_TURNS = 8