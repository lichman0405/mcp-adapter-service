# The code below is a Pydantic model for the MCP system, which includes the context, request, and response models.
# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class MCPContext(BaseModel):
    """
    MCPContext represents the context for a specific task in the MCP system.
    It includes the task ID, model identifier, user information, and any additional parameters.
    """
    task_id: str = Field(..., description="任务唯一标识")
    model: str = Field(..., description="后端服务标识，如 'maceopt', 'zeopp', 'xtb'")
    user: Optional[str] = Field(None, description="用户 ID（可选）")
    parameters: Optional[Dict[str, Any]] = Field({}, description="模型相关参数")


class MCPRequest(BaseModel):
    """
    MCPRequest represents a request to the MCP system.
    It includes the task ID, model identifier, user information, and the input data.
    """
    input: Any = Field(..., description="结构信息或上传内容")
    context: MCPContext = Field(..., description="任务上下文")


class MCPResponse(BaseModel):
    """
    MCPResponse represents the response from the MCP system.
    It includes the task ID, status, and any additional message.
    """
    task_id: str
    status: str = "PENDING"
    message: Optional[str] = None

if __name__ == "__main__":
    # Example usage
    context = MCPContext(task_id="12345", model="maceopt", user="user1", parameters={})
    print(context.model_dump_json())
    request = MCPRequest(input="example_structure", context=context)
    print(request.model_dump_json())
    response = MCPResponse(task_id="12345", status="COMPLETED", message="Task completed successfully.")
    print(response.model_dump_json())