import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from core.security import get_password_hash, verify_password
from database.schemas import (
    Message,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from database.models import User
from deps import SessionDep, CurrentUser, get_current_active_superuser
import database.crud.users

router = APIRouter(prefix="/users", tags=["users"])

SuperUser = Annotated[User, Depends(get_current_active_superuser)]


@router.get("/", dependencies=[Depends(get_current_active_superuser)], response_model=UsersPublic)
def read_users(db: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = db.execute(select(func.count()).select_from(User)).scalar_one()
    users = db.execute(select(User).offset(skip).limit(limit)).scalars().all()
    return UsersPublic(data=[UserPublic.model_validate(u) for u in users], count=count)


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
def create_user(*, db: SessionDep, user_in: UserCreate) -> Any:
    return database.crud.users.create_user(db, user_in)


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, db: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    return database.crud.users.update_user(db, current_user, user_in)


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, db: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    verified, _ = verify_password(body.current_password, current_user.hashed_password)
    if not verified:
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    current_user.hashed_password = get_password_hash(body.new_password)
    db.add(current_user)
    db.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(db: SessionDep, current_user: CurrentUser) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
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
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(*, db: SessionDep, user_id: uuid.UUID, user_in: UserUpdate) -> Any:
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return database.crud.users.update_user(db, db_user, user_in)


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    db: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    db.delete(user)
    db.commit()
    return Message(message="User deleted successfully")