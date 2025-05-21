# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Dispatcher logic that routes MCP tasks to the correct backend client based on model type.
"""

from app.models.schema import MCPRequest
from app.utils import logger
from app.services.task_queue import (
    run_maceopt_task,
    run_zeopp_task,
    run_xtb_task,
)


async def dispatch_task(mcp_request: MCPRequest) -> str:
    """
    Dispatch an MCP task to the corresponding backend based on model type.
    Returns a task_id after submitting to async task queue.
    """
    model = mcp_request.context.model.lower()
    logger.info(f"Dispatching task {mcp_request.context.task_id} to model '{model}'")

    if model == "maceopt":
        task = run_maceopt_task.delay(mcp_request.input, mcp_request.context.model_dump())
    elif model == "zeopp":
        task = run_zeopp_task.delay(mcp_request.input, mcp_request.context.model_dump())
    elif model == "xtb":
        task = run_xtb_task.delay(mcp_request.input, mcp_request.context.model_dump())
    else:
        raise ValueError(f"Unsupported model type: {model}")

    return task.id
