from fastapi import APIRouter, Depends, HTTPException, status
from backend.models import DocumentCreate, DocumentResponse
from backend.database import get_document_collection

from nlp.preprocessing import preprocess_text
from nlp.skill_extractor import extract_skills
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter()
docs_col = get_document_collection()

# Auth dependency to get current user (simplified for now, full JWT validation recommended)
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

@router.post("/", response_model=dict)
def upload_document(doc: DocumentCreate, current_user: str = Depends(get_current_user)):
    # Run NLP Pipeline (Milestone 2)
    processed_resume = preprocess_text(doc.resume_text)
    processed_jd = preprocess_text(doc.job_description)
    
    resume_skills = extract_skills(processed_resume)
    jd_skills = extract_skills(processed_jd)

    docs_col.insert_one({
        "user_email": current_user,
        "resume_text": doc.resume_text,
        "job_description": doc.job_description,
        
        # Store NLP Results
        "processed_resume": processed_resume,
        "processed_jd": processed_jd,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        
        "created_at": datetime.utcnow()
    })
    return {"message": "Document uploaded successfully"}

@router.get("/", response_model=List[dict])  # Simplified response model for list
def get_documents(current_user: str = Depends(get_current_user)):
    docs = list(docs_col.find({"user_email": current_user}))
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return docs
