from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    id: Optional[str] = Field(None, alias="_id")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class IngestionBase(BaseModel):
    user_id: str
    type: str  # 'resume' or 'jd'
    content: str
    filename: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class IngestionCreate(IngestionBase):
    pass
