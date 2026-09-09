import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Table, Column, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.base import Base
from backend.utilities.Mixins import AuditTrailMixin


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


task_tags = Table(
    "task_tags",
    Base.metadata,
    Column(
        "task_id",
        UUID(as_uuid=True),
        ForeignKey("tasks.task_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.tag_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Task(AuditTrailMixin, Base):
    __tablename__ = "tasks"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.category_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status_enum"),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, name="task_priority_enum"),
        default=TaskPriority.MEDIUM,
        nullable=False,
        index=True,
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    category: Mapped["Category | None"] = relationship(
        "Category", back_populates="tasks"
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=task_tags, back_populates="tasks"
    )
    reminders: Mapped[list["Reminder"]] = relationship(
        "Reminder", back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Task task_id={self.task_id} title={self.title!r}>"