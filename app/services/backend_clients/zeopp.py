# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-22

"""
Client module to interact with Zeo++ API backend for structure analysis.
Supports dynamic route selection via context.parameters.route.
Includes route whitelist enforcement, logging, and file safety.
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
    "pore_size_dist",
    "ray_tracing",
    "blocking_spheres",
    "distance_grid",
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

    route = parameters.get("route")
    if not route:
        route = "pore_diameter"
        logger.warning(f"[zeopp] Task {task_id} did not specify route. Using default: 'pore_diameter'")
    else:
        logger.info(f"[zeopp] Task {task_id} will use route: '{route}'")

    if route not in ZEO_SUPPORTED_ROUTES:
        raise ValueError(f"[zeopp] Unsupported Zeo++ route: '{route}'")

    output_filename = parameters.get("output_filename", f"{task_id}.res")
    base_url = settings.zeopp_base_url
    endpoint = f"{base_url}/api/{route}"

    logger.info(f"[zeopp] Dispatching task {task_id} to endpoint: {endpoint}")

    # 🛠 自动识别 input 格式：如果以 data_ 开头 → .cif，否则 → .cssr
    input_preview = input_data.strip().lower()
    suffix = ".cif" if input_preview.startswith("data_") else ".cssr"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w", encoding="utf-8") as tmp:
        tmp.write(input_data)
        tmp.flush()
        file_path = Path(tmp.name)

    try:
        with file_path.open("rb") as f:
            files = {
                "structure_file": (file_path.name, f, "text/plain")
            }
            data = {"output_filename": output_filename}

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(endpoint, files=files, data=data)

        if response.status_code != 200:
            raise RuntimeError(f"[zeopp] backend error: {response.status_code} - {response.text}")

        return response.json()

    finally:
        file_path.unlink(missing_ok=True)


def list_supported_routes() -> list:
    """
    Returns the list of available Zeo++ analysis routes.
    """
    return ZEO_SUPPORTED_ROUTES
