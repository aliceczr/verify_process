from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
from utils import rag_chain, get_llm, get_retriever
import time
import os
import uvicorn
from langsmith_client import get_client, create_run, finish_run_success, finish_run_error



start_time = time.time()



client = get_client()

app = FastAPI()

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
    groq_ok = bool(os.environ.get("GROQ_API_KEY"))
    status = "ok" if index_exists and groq_ok else "error"
    checks = {
        "faiss_index": "ok" if index_exists else "missing",
        "groq_api_key": "ok" if groq_ok else "missing",
    }
    return JSONResponse({
        "status": status,
        "uptime_seconds": int(uptime),
        "checks": checks
    }, status_code=(200 if status == "ok" else 500))


@app.post('/query', response_model=QueryOut)
async def query_model(query: QueryIn):

    try:

        run_id = create_run(client, name="query", prompt_text=query.content, metadata={"uid": query.uid})

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

        
        try:
            finish_run_success(client, run_id, output=answer or "", extra_metadata={"duration_ms": duration_ms})
        except Exception:
            logging.exception("Error finishing LangSmith run")

        return QueryOut(
            uid=query.uid,
            response=answer,
            sources=sources
        )

    except Exception as e:
        logging.exception("Error processing request")
        
        try:
            finish_run_error(client, locals().get('run_id'), error_message=str(e), extra_metadata=None)
        except Exception:
            logging.exception("Error finishing LangSmith run on exception")
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

if __name__ == '__main__':
      uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")


