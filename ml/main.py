from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from utils import rag_chain
import time
import os
import uvicorn

from config import GROQ_API_KEY, LANGSMITH_API_KEY, LANGCHAIN_TRACING_V2, LANGCHAIN_PROJECT

start_time = time.time()

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryIn(BaseModel):
    uid: str | None = None
    content: str

class QueryOut(BaseModel):
    uid: str | None = None
    response: str
    sources: list[dict] = []

@app.get("/health")
def health():
    uptime = time.time() - start_time
    index_exists = os.path.exists("vector_store/faiss_index/index.faiss")
    groq_ok = bool(GROQ_API_KEY)
    langsmith_ok = bool(LANGSMITH_API_KEY)
    
    status = "ok" if index_exists and groq_ok else "error"
    checks = {
        "faiss_index": "ok" if index_exists else "missing",
        "groq_api_key": "ok" if groq_ok else "missing",
        "langsmith_tracing": "ok" if langsmith_ok and LANGCHAIN_TRACING_V2 else "disabled",
        "langsmith_project": LANGCHAIN_PROJECT if LANGCHAIN_PROJECT else "missing"
    }
    return JSONResponse({
        "status": status,
        "uptime_seconds": int(uptime),
        "checks": checks
    }, status_code=(200 if status == "ok" else 500))

@app.post('/query', response_model=QueryOut)
async def query_model(query: QueryIn):
    try:
        logger.info(f"Processing query with LangSmith tracing: {LANGCHAIN_TRACING_V2}")
        logger.info(f"LangSmith project: {LANGCHAIN_PROJECT}")

        start = time.time()

        
        chain = rag_chain()
        result = chain.invoke({
            "input": query.content,
            "chat_history": []
        })
       
        answer = result.get("answer") or result.get("result")
        docs = result.get("source_documents", [])

        sources = [
            {
                "content": d.page_content,
                "metadata": d.metadata
            }
            for d in docs
        ]

        duration_ms = int((time.time() - start) * 1000)
        logger.info(f"Request processed in {duration_ms}ms")

        return QueryOut(
            uid=query.uid,
            response=answer,
            sources=sources
        )

    except Exception as e:
        logger.exception("Error processing request")
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)