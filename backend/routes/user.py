from fastapi import APIRouter, HTTPException
from database.schemas import UserCreate, UserRegister, UserPublic, Message
from database.models import User
from typing import Any
import uuid
from deps import SessionDep, CurrentUser
import database.crud.users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(*, db: SessionDep, user_in: UserCreate) -> Any:
    return database.crud.users.create_user(db, user_in)


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(current_user: CurrentUser, db: SessionDep) -> Any:
    db.delete(current_user)
    db.commit()
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(db: SessionDep, user_in: UserRegister) -> Any:
    user_create = UserCreate.model_validate(user_in)
    return database.crud.users.create_user(db, user_create)


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, db: SessionDep, current_user: CurrentUser
) -> Any:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user != current_user:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return user

