import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "")
API_URL = os.getenv("API_URL", "http://localhost:8000")

