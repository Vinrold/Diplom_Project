from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserLogin, Token
from app.config import settings
from app.security import verify_password, create_access_token

router = APIRouter(
    # начало эндпоинтов - префикс
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    return {"access_token":access_token, "token_type": "bearer"}
