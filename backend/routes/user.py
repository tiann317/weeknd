from fastapi import APIRouter, Depends, HTTPException
from database.schemas import UserCreate, UserPublic
from typing import Any
from sqlalchemy.orm import Session
from deps import get_db
import database.crud.users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    user = database.crud.users.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = database.crud.users.create_user(db, user_in)
    return user
