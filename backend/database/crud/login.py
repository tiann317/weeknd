from fastapi import Depends
from deps import get_db
from sqlalchemy.orm import Session
from core.security import verify_password
from .users import get_user_by_email
from database.models import User

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(
    email: str, password: str, db: Session = Depends(get_db)
) -> User | None:
    db_user = get_user_by_email(db, email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
