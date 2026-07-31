from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, UUID as sa_UUID

from backend.core.base import Base

class User(Base):
    __tablename__="user"

    user_id : Mapped[UUID] = Column(sa_UUID, primary_key=True, index = True, nullable=False, default=uuid4())
    user_name : Mapped[str] = Column(String, nullable=False)
     
