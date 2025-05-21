# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
FastAPI application entry point for the MCP Adapter.
Defines the /mcp and /result endpoints and integrates middleware and dispatcher.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.models.schema import MCPRequest, MCPResponse
from app.adapters.dispatcher import dispatch_task
from celery.result import AsyncResult
from app.services.task_queue import celery_app
from app.services.backend_clients.zeopp import list_supported_routes

app = FastAPI(title="MCP Adapter Service")

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/mcp", response_model=MCPResponse)
async def handle_mcp(request: MCPRequest):
    """
    Receives an MCP request and dispatches it to the correct backend service.
    """
    task_id = await dispatch_task(request)
    return MCPResponse(task_id=task_id, status="PENDING")


@app.get("/result/{task_id}")
def get_result(task_id: str):
    """
    Retrieve the status and result of a given task ID.
    """
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"task_id": task_id, "status": "PENDING"}
    elif result.state == "STARTED":
        return {"task_id": task_id, "status": "IN_PROGRESS"}
    elif result.state == "FAILURE":
        return {"task_id": task_id, "status": "FAILED", "error": str(result.result)}
    elif result.state == "SUCCESS":
        return result.result
    else:
        return {"task_id": task_id, "status": result.state}


@app.get("/zeopp/list_routes")
def get_zeopp_supported_routes():
    """
    Returns the list of all supported Zeo++ analysis routes.
    """
    return {
        "model": "zeopp",
        "supported_routes": list_supported_routes()
    }
