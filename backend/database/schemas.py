from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
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
