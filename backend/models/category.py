import uuid
import enum
from datetime import datetime
 
from sqlalchemy import (
    String, Text, Boolean, DateTime, ForeignKey, Enum, Table, Column, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from backend.core.base import Base
from backend.utilities.Mixins import AuditTrailMixin
 
class Category(AuditTrailMixin, Base):
    __tablename__ = "categories"
 
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    category_name: Mapped[str] = mapped_column(String(50), nullable=False)
    category_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
 
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")
 