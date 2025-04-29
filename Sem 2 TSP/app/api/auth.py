from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.cruds.user import get_user_by_email, create_user, verify_password
from app.core.security import create_access_token, decode_access_token
from app.db.session import get_db
from app.models.user import User
from typing import List  # Добавляем для аннотации списка

router = APIRouter()

@router.post("/sign-up/", response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user.email, user.password)
    token = create_access_token({"sub": str(new_user.id)})
    return {"id": new_user.id, "email": new_user.email, "token": token}

@router.post("/login/", response_model=UserResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"id": db_user.id, "email": db_user.email, "token": token}

@router.get("/users/me/", response_model=UserResponse)
def get_me(token: str = Depends(lambda x: x.headers.get("Authorization").split(" ")[1]), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": db_user.id, "email": db_user.email, "token": token}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/users/", response_model=List[UserResponse])  # Новый эндпоинт
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "email": user.email, "token": create_access_token({"sub": str(user.id)})} for user in users]