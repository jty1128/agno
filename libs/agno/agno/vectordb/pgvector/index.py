from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Ivfflat(BaseModel):
    name: str | None = None
    lists: int = 100
    probes: int = 10
    dynamic_lists: bool = True
    configuration: dict[str, Any] = Field(default_factory=lambda: {"maintenance_work_mem": "2GB"})


class HNSW(BaseModel):
    name: str | None = None
    m: int = 16
    ef_search: int = 5
    ef_construction: int = 200
    configuration: dict[str, Any] = Field(default_factory=lambda: {"maintenance_work_mem": "2GB"})
