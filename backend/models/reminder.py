import uuid
import enum
from datetime import datetime
 
from sqlalchemy import (
    String, Text, Boolean, DateTime, ForeignKey, Enum, Table, Column, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from backend.core.base import Base


class ReminderType(str, enum.Enum):
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
 
 
class Reminder(Base):
    __tablename__ = "reminders"
 
    reminder_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.task_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
 
    remind_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    reminder_type: Mapped[ReminderType] = mapped_column(
        Enum(ReminderType, name="reminder_type_enum"),
        default=ReminderType.IN_APP,
        nullable=False,
    )
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
 
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
 
    task: Mapped["Task"] = relationship("Task", back_populates="reminders")
 
    def __repr__(self) -> str:
        return f"<Reminder reminder_id={self.reminder_id} remind_at={self.remind_at}>"
 
