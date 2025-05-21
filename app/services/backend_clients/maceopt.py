# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Client module to interact with the MACEOPT backend FastAPI service.
Performs async POST multipart/form-data requests to the /optimize endpoint.
"""

import httpx
import tempfile
from pathlib import Path
from typing import Dict, Any
from app.config import settings
from app.utils import logger

async def call_backend(input_data: str, context: Dict[str, Any]) -> Dict:
    """
    Calls the MACEOPT backend service to perform structure optimization.
    
    :param input_data: Structure string (e.g., .xyz file content)
    :param context: Dict including task_id, parameters (e.g., fmax, device)
    :return: Parsed response from backend
    """
    base_url = settings.maceopt_base_url
    endpoint = f"{base_url}/optimize"
    params = context.get("parameters", {})
    task_id = context.get("task_id", "unknown")

    # Write input string to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xyz") as tmp:
        tmp.write(input_data.encode())
        tmp.flush()
        file_path = Path(tmp.name)

    files = {"structure_file": (file_path.name, file_path.open("rb"), "text/plain")}
    data = {}

    if "fmax" in params:
        data["fmax"] = str(params["fmax"])
    if "device" in params:
        data["device"] = params["device"]

    logger.info(f"[maceopt] Sending request to backend for task {task_id}")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(endpoint, data=data, files=files)

    file_path.unlink(missing_ok=True)

    if response.status_code != 200:
        raise RuntimeError(f"Backend error [{response.status_code}]: {response.text}")

    return response.json()
