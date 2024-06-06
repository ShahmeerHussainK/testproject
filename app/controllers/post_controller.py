from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import PostCreate, Post
from app.services.post_service import PostService
from app.database import SessionLocal
from app.services.auth_service import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/posts", response_model=Post)
def add_post(post: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if len(post.text.encode('utf-8')) > 1048576:
        raise HTTPException(status_code=400, detail="Post exceeds 1 MB size limit")
    return PostService.add_post(db, post, user)


@router.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return PostService.get_posts(db, user)


@router.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return PostService.delete_post(db, post_id, user)
