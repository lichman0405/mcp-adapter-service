# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Client module to interact with Zeo++ API backend for pore and surface analysis.
Supports dynamic route selection via context.parameters.route.
Includes route whitelist enforcement.
"""

import httpx
from typing import Dict, Any
from app.config import settings
from app.utils import logger
import tempfile
from pathlib import Path

# Supported Zeo++ routes (based on actual FastAPI service)
ZEO_SUPPORTED_ROUTES = [
    "pore_diameter",
    "surface_area",
    "accessible_volume",
    "probe_volume",
    "channel_analysis",
    "structure_info",
    "oms_detection",
    "pore_size_dist",
    "ray_tracing",
    "blocking_spheres",
    "distance_grid",
    "convert_xyz",
    "voronoi_network"
]


async def call_backend(input_data: str, context: Dict[str, Any]) -> Dict:
    """
    Calls the Zeo++ backend for a specific analysis route.
    
    :param input_data: Structure file content (.cssr or .cif)
    :param context: Dict with task_id and parameters (including 'route')
    :return: Parsed response from Zeo++ backend
    """
    task_id = context.get("task_id", "unknown")
    parameters = context.get("parameters", {})
    route = parameters.get("route", "pore_diameter")  # default route

    if route not in ZEO_SUPPORTED_ROUTES:
        raise ValueError(f"Unsupported Zeo++ route: {route}")

    output_filename = parameters.get("output_filename", f"{task_id}.res")
    base_url = settings.zeopp_base_url
    endpoint = f"{base_url}/api/{route}"

    logger.info(f"[zeopp] Dispatching task {task_id} to {endpoint}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".cssr") as tmp:
        tmp.write(input_data.encode())
        tmp.flush()
        file_path = Path(tmp.name)

    files = {
        "structure_file": (file_path.name, file_path.open("rb"), "text/plain")
    }
    data = {"output_filename": output_filename}

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(endpoint, files=files, data=data)

    file_path.unlink(missing_ok=True)

    if response.status_code != 200:
        raise RuntimeError(f"[zeopp] backend error: {response.text}")

    return response.json()


def list_supported_routes() -> list:
    """
    Returns the list of available Zeo++ analysis routes.
    """
    return ZEO_SUPPORTED_ROUTES
