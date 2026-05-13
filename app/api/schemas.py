from datetime import datetime
from pydantic import BaseModel


class ScanCreateRequest(BaseModel):
    target: str
    fast_mode: bool = False
    output_dir: str = "results"


class ScanJobResponse(BaseModel):
    id: int
    target: str
    status: str
    fast_mode: bool
    output_dir: str
    findings_json: dict
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True
