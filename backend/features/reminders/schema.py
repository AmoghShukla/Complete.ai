from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.models.reminder import ReminderType


class ReminderCreate(BaseModel):
    remind_at: datetime
    reminder_type: ReminderType = ReminderType.IN_APP


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reminder_id: UUID
    task_id: UUID
    remind_at: datetime
    reminder_type: ReminderType
    is_sent: bool
    sent_at: datetime | None
    created_at: datetime


class ReminderListResponse(BaseModel):
    items: list[ReminderResponse]
    total: int