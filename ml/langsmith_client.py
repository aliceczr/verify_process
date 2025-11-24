import os
import uuid
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("ml.langsmith")

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")


def get_client() -> Optional[Any]:
 
    if not LANGSMITH_API_KEY:
        logger.debug("LANGSMITH_API_KEY not set; LangSmith disabled")
        return None

    try:
        import langsmith
    except Exception as e:  
        logger.warning("langsmith package not available: %s", e)
        return None

   
    try:
        Client = getattr(langsmith, "Client", None)
        if Client:
            return Client(api_key=LANGSMITH_API_KEY)

      
        create_client = getattr(langsmith, "create_client", None)
        if create_client:
            return create_client(api_key=LANGSMITH_API_KEY)

    except Exception as e:  
        logger.exception("error constructing langsmith client: %s", e)

    logger.warning("could not create LangSmith client (unsupported SDK shape)")
    return None


def create_run(client: Optional[Any], name: str, prompt_text: str, metadata: Dict[str, Any]) -> str:
    """Create a run record and return a run_id.

    If a real client exists, attempt to create a run remotely; otherwise
    generate a local UUID and return it. Errors are swallowed to avoid
    interrupting the main flow.
    """
    run_id = str(uuid.uuid4())
    if not client:
        logger.debug("LangSmith disabled: created local run_id %s", run_id)
        return run_id

    try:
     
        if hasattr(client, "create_run"):

            obj = client.create_run(name=name, prompt=prompt_text, metadata=metadata)
  
            return getattr(obj, "id", run_id) or run_id

        if hasattr(client, "runs") and hasattr(client.runs, "create"):
            obj = client.runs.create(name=name, prompt=prompt_text, metadata=metadata)
            return getattr(obj, "id", run_id) or run_id

  
        logger.debug("LangSmith client present but no known create API; using local id")
        return run_id

    except Exception as e:
        logger.exception("failed to create langsmith run: %s", e)
        return run_id


def finish_run_success(client: Optional[Any], run_id: Optional[str], output: str, extra_metadata: Dict[str, Any] | None = None) -> None:
    if not client or not run_id:
        logger.debug("LangSmith finish success skipped (no client or run_id)")
        return
    try:
        if hasattr(client, "finish_run"):
            client.finish_run(run_id, status="succeeded", output=output, metadata=extra_metadata or {})
            return
        if hasattr(client, "runs") and hasattr(client.runs, "finish"):
            client.runs.finish(run_id, status="succeeded", output=output, metadata=extra_metadata or {})
            return
    except Exception as e:
        logger.exception("error finishing langsmith run success: %s", e)


def finish_run_error(client: Optional[Any], run_id: Optional[str], error_message: str, extra_metadata: Dict[str, Any] | None = None) -> None:
    if not client or not run_id:
        logger.debug("LangSmith finish error skipped (no client or run_id)")
        return
    try:
        if hasattr(client, "finish_run"):
            client.finish_run(run_id, status="failed", error=error_message, metadata=extra_metadata or {})
            return
        if hasattr(client, "runs") and hasattr(client.runs, "finish"):
            client.runs.finish(run_id, status="failed", error=error_message, metadata=extra_metadata or {})
            return
    except Exception as e:
        logger.exception("error finishing langsmith run error: %s", e)
