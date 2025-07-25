from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database.session import get_db
from app.models.user import User
from app.core.security import get_password_hash, verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.schemas.user import UserCreate
from jose import jwt, JWTError


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user