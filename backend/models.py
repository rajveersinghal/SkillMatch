from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentCreate(BaseModel):
    resume_text: str
    job_description: str

class DocumentResponse(BaseModel):
    id: str
    user_email: str
    resume_text: str
    job_description: str
    
    # NLP Fields (Milestone 2)
    processed_resume: Optional[str] = None
    processed_jd: Optional[str] = None
    resume_skills: list[str] = []
    jd_skills: list[str] = []
    
    created_at: datetime
