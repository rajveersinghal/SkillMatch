from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Any

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SkillSchema(BaseModel):
    skill: str

class DocumentResponse(BaseModel):
    id: str
    user_email: str
    resume_filename: Optional[str] = None
    resume_text: str
    job_description: str
    
    # NLP & AI Fields
    match_percentage: float
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    gap_analysis: Optional[dict[str, list[str]]] = None
    suggestions: list[str] = []
    insights: Optional[dict[str, Any]] = None
    
    created_at: datetime
    timestamp: datetime
