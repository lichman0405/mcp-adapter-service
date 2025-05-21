# The code below is a logger utility for the MCP system, which uses the Rich library for enhanced logging.
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Rich logger with trace ID support for unified logging across the MCP system.
"""

from rich.console import Console
from rich.logging import RichHandler
import logging
from app.utils.trace import get_trace_id

console = Console()
FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("mcp")

def log_with_trace(level: str, message: str):
    """
    Log a message with the current trace ID.
    Args:
        level (str): The logging level (e.g., 'info', 'error').
        message (str): The message to log.
    Returns:
        None
    """
    trace_id = get_trace_id()
    formatted = f"[trace {trace_id}] {message}" if trace_id else message
    getattr(logger, level)(formatted)

# Semantic log levels
def info(msg: str): log_with_trace("info", msg)
def success(msg: str): log_with_trace("info", f"[green]✔ {msg}[/green]")
def error(msg: str): log_with_trace("error", f"[red]✘ {msg}[/red]")
def debug(msg: str): log_with_trace("debug", msg)
