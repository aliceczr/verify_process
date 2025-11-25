import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "default")