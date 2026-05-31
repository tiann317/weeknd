from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(User):
    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    created_at: datetime | None = None
    id: uuid.UUID


