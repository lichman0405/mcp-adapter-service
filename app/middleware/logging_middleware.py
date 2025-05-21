# The code below is a FastAPI middleware for logging incoming requests and injecting trace IDs.
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
FastAPI middleware for injecting trace ID and logging incoming requests.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.utils.trace import generate_trace_id, set_trace_id
from app.utils import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that injects a trace ID into the request context and logs incoming requests.
    It generates a new trace ID if not provided in the request headers.
    Args:
        app: The FastAPI application instance.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate and set trace ID
        trace_id = request.headers.get("X-Trace-Id") or generate_trace_id()
        set_trace_id(trace_id)

        logger.info(f"Incoming request: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            logger.success(f"Handled request: {request.url.path} → Status {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Unhandled error in {request.url.path}: {e}")
            raise e
