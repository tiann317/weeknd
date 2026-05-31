from sqlalchemy import update, select
from sqlalchemy.orm import Session
from database.models import User
from database.schemas import UserCreate
from core.security import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = db.execute(statement).scalars().first()
    return session_user
