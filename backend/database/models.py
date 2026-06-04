# backend/database/models.py
import uuid
from sqlalchemy import VARCHAR, Boolean, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
