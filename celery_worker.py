# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Celery worker entry point to process asynchronous MCP backend dispatch tasks.
Run this file with a worker process.
"""

from app.services.task_queue import celery_app

# This ensures task registration when the worker is started
# Usage: celery -A celery_worker.celery_app worker --loglevel=info
