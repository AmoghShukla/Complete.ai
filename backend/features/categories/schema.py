from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=50)
    category_color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None, min_length=1, max_length=50)
    category_color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: UUID
    user_id: UUID
    category_name: str
    category_color: str | None
    created_at: datetime
    updated_at: datetime


class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]
    total: int