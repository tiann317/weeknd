from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database.models import User
from database.schemas import UserCreate, UserUpdate, UserUpdateMe
from core.security import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )
    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate | UserUpdateMe) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalars().first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.execute(select(User).where(User.username == username)).scalars().first()
