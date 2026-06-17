import enum
import uuid
from sqlalchemy import VARCHAR, Boolean, ForeignKey, func, DateTime
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB, UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)


class SportType(str, enum.Enum):
    hike = "hike"
    bike = "bike"
    run = "run"


class Station(Base):
    __tablename__ = "stations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(200))
    lat: Mapped[float]
    lon: Mapped[float]
    db_eva_id: Mapped[str | None] = mapped_column(VARCHAR(20))
    operator: Mapped[str | None] = mapped_column(VARCHAR(120))
    is_private_railway: Mapped[bool] = mapped_column(default=False)
    dticket_valid: Mapped[bool] = mapped_column(default=True)


class Hike(Base):
    __tablename__ = "hikes"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(VARCHAR(200))
    description: Mapped[str | None] = mapped_column(VARCHAR(250))
    sport: Mapped[SportType] = mapped_column(
        sqlalchemy.Enum(SportType, name="sport_type"), default=SportType.hike
    )
    distance_km: Mapped[float]
    duration_min: Mapped[int]
    ascent_m: Mapped[int | None]
    difficulty: Mapped[str | None] = mapped_column(VARCHAR(20))  # easy | moderate | hard
    start_lat: Mapped[float]
    start_lon: Mapped[float]
    end_lat: Mapped[float | None]
    end_lon: Mapped[float | None]
    is_loop: Mapped[bool] = mapped_column(default=True)
    geometry: Mapped[dict | None] = mapped_column(JSONB)
    region: Mapped[str] = mapped_column(VARCHAR(80), index=True)
    start_station_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("stations.id"))
    end_station_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("stations.id"))
    source_url: Mapped[str | None] = mapped_column(VARCHAR(500))
    attribution: Mapped[str | None] = mapped_column(VARCHAR(200))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    start_station: Mapped["Station | None"] = relationship(foreign_keys=[start_station_id])
    end_station: Mapped["Station | None"] = relationship(foreign_keys=[end_station_id])
