from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
from database.models import SportType
import uuid


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(User):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    is_superuser: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(UserBase):
    is_active: bool
    is_superuser: bool
    created_at: datetime
    id: uuid.UUID


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


class UserUpdateMe(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = None


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: uuid.UUID


class Message(BaseModel):
    message: str


class HikeListItem(BaseModel):
    id: uuid.UUID
    title: str
    sport: SportType
    distance_km: float
    duration_min: int
    region: str
    start_lat: float
    start_lon: float
    model_config = ConfigDict(from_attributes=True)


class StationRead(BaseModel):
    name: str
    operator: str | None
    is_private_railway: bool
    model_config = ConfigDict(from_attributes=True)


class HikeDetail(HikeListItem):
    description: str | None
    ascent_m: int | None
    end_lat: float | None
    end_lon: float | None
    is_loop: bool
    geometry: dict | None
    start_station: StationRead | None
    end_station: StationRead | None
    source_url: str | None
    attribution: str | None
