# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Simple routing strategy for MCP backend service selection.
Currently returns single static URL per model.
"""

from app.adapters.registry import get_service_url

def choose_backend_instance(model: str) -> str:
    """
    Choose one backend instance for a given model.
    Placeholder for load balancing logic (currently static).
    """
    return get_service_url(model)
