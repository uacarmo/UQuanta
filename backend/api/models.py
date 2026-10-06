from typing import Any

from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    experiment: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class JobResponse(BaseModel):
    job_id: str
    status: str


class AxisData(BaseModel):
    name: str
    unit: str
    values: list[float]


class ExperimentData(BaseModel):
    x: AxisData
    y: AxisData


class ExperimentResult(BaseModel):
    experiment: str
    result_type: str
    data: ExperimentData
    metadata: dict[str, Any] = Field(default_factory=dict)