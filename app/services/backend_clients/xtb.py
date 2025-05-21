# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Client module to interact with xTB geometry optimization backend.
"""

import httpx
from typing import Dict, Any
from app.config import settings
from app.utils import logger
import tempfile
from pathlib import Path


async def call_backend(input_data: str, context: Dict[str, Any]) -> Dict:
    """
    Calls the xTB backend service to perform geometry optimization.
    """
    task_id = context.get("task_id", "unknown")
    base_url = settings.xtb_base_url
    endpoint = f"{base_url}/optimize"
    params = context.get("parameters", {})

    logger.info(f"[xtb] Dispatching task {task_id} to {endpoint}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xyz") as tmp:
        tmp.write(input_data.encode())
        tmp.flush()
        file_path = Path(tmp.name)

    files = {"file": (file_path.name, file_path.open("rb"), "text/plain")}
    data = {
        "charge": str(params.get("charge", 0)),
        "uhf": str(params.get("uhf", 0)),
        "gfn": str(params.get("gfn", 1)),
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(endpoint, files=files, data=data)

    file_path.unlink(missing_ok=True)

    if response.status_code != 200:
        raise RuntimeError(f"[xtb] backend error: {response.text}")

    return response.json()
