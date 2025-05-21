# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Trace ID utilities for request context tracing across distributed services.
"""

import uuid
import contextvars

# ContextVar to store trace ID per request
trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")


def generate_trace_id() -> str:
    """
    Generate a new trace ID.
    args:
        None
    returns:
        str: A new trace ID.
    """
    return str(uuid.uuid4())


def set_trace_id(trace_id: str):
    """
    Set the current trace ID.
    args:
        trace_id (str): The trace ID to set.
    returns:
        None
    """
    trace_id_var.set(trace_id)


def get_trace_id() -> str:
    """
    Retrieve the current trace ID.
    args:
        None
    returns:
        str: The current trace ID.
    raises:
        LookupError: If the trace ID is not set in the context.
    """
    return trace_id_var.get()
