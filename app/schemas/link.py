from datetime import datetime

from pydantic import BaseModel, ConfigDict, AnyHttpUrl


class LinkCreate(BaseModel):
    original_url: AnyHttpUrl


class LinkRead(BaseModel):
    original_url: str
    code: str
    clicks: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
