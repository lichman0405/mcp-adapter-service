# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-21

"""
Global configuration module using Pydantic v2-compatible BaseSettings.
Loads from .env file or environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    App-wide configuration, loaded from environment or .env file.
    """
    redis_url: str = Field("redis://localhost:6379/0", description="Redis 连接地址")
    celery_broker_url: str = Field("redis://localhost:6379/0", description="Celery 消息队列")
    celery_result_backend: str = Field("redis://localhost:6379/0", description="Celery 结果存储")

    maceopt_base_url: str = Field("http://maceopt:4748", description="MACEOPT 服务地址")
    zeopp_base_url: str = Field("http://zeopp:8000", description="Zeo++ 服务地址")
    xtb_base_url: str = Field("http://xtbopt:8000", description="xTB 服务地址")

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()


