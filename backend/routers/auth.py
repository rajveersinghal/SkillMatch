from fastapi import APIRouter, HTTPException, Depends, status
from backend.models import UserRegister, UserLogin, Token
from backend.database import get_user_collection
from core.utils import hash_password, verify_password
from datetime import datetime, timedelta
import os
from jose import jwt

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    users_col = get_user_collection()
    if users_col is None:
        raise HTTPException(status_code=503, detail="Database connection failed. Please check MONGO_URI.")
        
    if users_col.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    users_col.insert_one({
        "email": user.email,
        "password": hashed,
        "created_at": datetime.utcnow()
    })
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    users_col = get_user_collection()
    if users_col is None:
        raise HTTPException(status_code=503, detail="Database connection failed. Please check MONGO_URI.")
        
    db_user = users_col.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
