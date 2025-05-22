# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-22

"""
Client module to interact with Zeo++ API backend for structure analysis.
Uses zeopp_routes.json to dynamically determine required parameters.
"""

import httpx
from typing import Dict, Any
from app.config import settings
from app.utils import logger
import tempfile
from pathlib import Path
import json

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

# Load route schema (you must place zeopp_routes.json in project root or alongside this script)
ZEO_ROUTE_CONFIG_PATH = Path(__file__).parent.parent / "zeopp_routes.json"
if not ZEO_ROUTE_CONFIG_PATH.exists():
    raise FileNotFoundError(f"Zeo++ route schema not found: {ZEO_ROUTE_CONFIG_PATH}")
ZEO_ROUTE_CONFIG = json.loads(ZEO_ROUTE_CONFIG_PATH.read_text(encoding="utf-8"))


async def call_backend(input_data: str, context: Dict[str, Any]) -> Dict:
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

            # 🔁 Dynamic parameter injection based on zeopp_routes.json
            route_schema = ZEO_ROUTE_CONFIG.get(route)
            if not route_schema:
                raise ValueError(f"[zeopp] No schema defined for route: '{route}'")

            data = {}
            for key in route_schema.get("required", []):
                if key not in parameters:
                    raise ValueError(f"[zeopp] Missing required Zeo++ param: '{key}'")
                data[key] = str(parameters[key])

            for key in route_schema.get("optional", []):
                if key in parameters:
                    val = parameters[key]
                    data[key] = str(val).lower() if isinstance(val, bool) else str(val)

            data["output_filename"] = output_filename  # always include if available

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(endpoint, files=files, data=data)

        if response.status_code != 200:
            raise RuntimeError(f"[zeopp] backend error: {response.status_code} - {response.text}")

        return response.json()

    finally:
        file_path.unlink(missing_ok=True)


def list_supported_routes() -> list:
    return ZEO_SUPPORTED_ROUTES
