import uuid
import enum
from datetime import datetime
 
from sqlalchemy import (
    String, Text, Boolean, DateTime, ForeignKey, Enum, Table, Column, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from backend.core.base import Base

class Tag(Base):
    __tablename__ = "tags"
 
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False, 
        index=True
    )
 
    tag_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
 
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
 
    tasks: Mapped[list["Task"]] = relationship("Task", secondary=task_tags, back_populates="tags")
 
    def __repr__(self) -> str:
        return f"<Tag tag_id={self.tag_id} name={self.tag_name!r}>"