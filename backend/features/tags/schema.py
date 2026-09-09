from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    tag_name: str = Field(..., min_length=1, max_length=100)


class TagUpdate(BaseModel):
    tag_name: str = Field(..., min_length=1, max_length=100)


class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag_id: UUID
    user_id: UUID
    tag_name: str
    created_at: datetime
    updated_at: datetime


class TagListResponse(BaseModel):
    items: list[TagResponse]
    total: int