# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Service registry module for retrieving backend API addresses based on model name.
Uses global settings loaded from .env via config.py.
"""

from app.config import settings


REGISTERED_SERVICES = {
    "maceopt": settings.maceopt_base_url,
    "zeopp": settings.zeopp_base_url,
    "xtb": settings.xtb_base_url,
}


def get_service_url(model: str) -> str:
    """
    Retrieve the base URL of the registered backend service for a given model.
    Raises an error if the model is not found.
    """
    model = model.lower()
    if model not in REGISTERED_SERVICES:
        raise ValueError(f"Model '{model}' not registered.")
    return REGISTERED_SERVICES[model]
