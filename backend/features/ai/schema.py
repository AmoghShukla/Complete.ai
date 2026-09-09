from datetime import datetime

from pydantic import BaseModel, Field

from backend.models.task import TaskPriority, TaskStatus


class TaskParseRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=4000)


class ParsedTask(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None
    category_name: str | None = None
    tags: list[str] = Field(default_factory=list, max_length=20)


class TaskParseResponse(BaseModel):
    input_text: str
    task: ParsedTask