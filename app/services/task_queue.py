# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Asynchronous task queue using Celery to handle MCP backend dispatching.
Each task submits the request to the correct backend and returns results.
"""

import asyncio
from celery import Celery
from app.config import settings
from app.utils import logger
from app.services.backend_clients import maceopt, zeopp, xtb

celery_app = Celery(
    "mcp_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task(name="run_maceopt_task")
def run_maceopt_task(input_data, context: dict):
    task_id = context.get("task_id", "unknown")
    logger.info(f"Start MACEOPT task {task_id}")
    try:
        result = asyncio.run(maceopt.call_backend(input_data, context))
        return {"task_id": task_id, "status": "COMPLETED", "result": result}
    except Exception as e:
        logger.error(f"MACEOPT task {task_id} failed: {e}")
        return {"task_id": task_id, "status": "FAILED", "message": str(e)}


@celery_app.task(name="run_zeopp_task")
def run_zeopp_task(input_data, context: dict):
    task_id = context.get("task_id", "unknown")
    logger.info(f"Start Zeo++ task {task_id}")
    try:
        result = asyncio.run(zeopp.call_backend(input_data, context))
        return {"task_id": task_id, "status": "COMPLETED", "result": result}
    except Exception as e:
        logger.error(f"Zeo++ task {task_id} failed: {e}")
        return {"task_id": task_id, "status": "FAILED", "message": str(e)}


@celery_app.task(name="run_xtb_task")
def run_xtb_task(input_data, context: dict):
    task_id = context.get("task_id", "unknown")
    logger.info(f"Start xTB task {task_id}")
    try:
        result = asyncio.run(xtb.call_backend(input_data, context))
        return {"task_id": task_id, "status": "COMPLETED", "result": result}
    except Exception as e:
        logger.error(f"xTB task {task_id} failed: {e}")
        return {"task_id": task_id, "status": "FAILED", "message": str(e)}
