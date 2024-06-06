from MySQLdb import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, User, UserLogin
from app.services.auth_service import signup,login,get_current_user
from app.database import SessionLocal, get_db

router = APIRouter()

@router.post("/signup", response_model=User)
def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = signup(db, user)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.post("/login")
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    token = login(db, user)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": token}
