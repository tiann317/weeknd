from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(User):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(UserBase):
    is_active: bool
    created_at: datetime
    id: uuid.UUID


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: uuid.UUID


class Message(BaseModel):
    message: str
