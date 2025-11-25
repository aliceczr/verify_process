# langsmith_client.py
import os
import logging
from typing import Optional, Any

logger = logging.getLogger("langsmith")

def get_traceable():
    """Return traceable decorator if available, otherwise no-op decorator."""
    try:
        from langsmith import traceable
        logger.info("LangSmith traceable decorator available")
        return traceable
    except ImportError:
        logger.warning("LangSmith not available, using no-op traceable")
        def noop_traceable(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
        return noop_traceable
    except Exception as e:
        logger.error(f"Error initializing LangSmith traceable: {e}")
        def noop_traceable(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
        return noop_traceable