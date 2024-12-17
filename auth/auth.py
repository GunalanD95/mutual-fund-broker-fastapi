from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import User
from datetime import datetime, timedelta
from dotenv import load_dotenv

import bcrypt
import jwt
import os

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
load_dotenv()

class UserCreate(BaseModel):
    name:str
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    pwd_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_obj = User(
        name=user.name,
        email=user.email,
        password=pwd_hash.decode('utf-8')
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {
        "message": "User registered successfully",
    }
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_obj = db.query(User).filter(User.email == user.email).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid user found"
        )
    is_valid_password = bcrypt.checkpw(user.password.encode('utf-8'), user_obj.password.encode('utf-8'))
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid password"
        )
    payload = {
        "user_id": str(user_obj.id),
        "email": user_obj.email,
        "exp": datetime.utcnow() + timedelta(hours=1)  
    }

    token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
    return {
        "token": token,
        "message": "Login successful"
    }
        
    
