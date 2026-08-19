from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class AuditTrailMixin:

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_deleted : Mapped[bool] = mapped_column(Boolean, default=False)

