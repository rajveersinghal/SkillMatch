from fastapi import APIRouter, Depends, HTTPException, status
from backend.models import DocumentCreate, DocumentResponse
from backend.database import get_document_collection

from nlp.preprocessing import preprocess_text
from nlp.skill_extractor import extract_skills
from nlp.vectorizer import generate_tfidf_vectors
from nlp.matcher import calculate_match_score, identify_skill_gap, group_skills_by_category
from nlp.suggestion_engine import SuggestionEngine
from data.skill_taxonomy import skill_taxonomy
from core.usage_stats import update_stats

from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter()
docs_col = get_document_collection()
suggestion_engine = SuggestionEngine()


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
    try:
        # Run NLP Pipeline (Milestone 2)
        processed_resume = preprocess_text(doc.resume_text)
        processed_jd = preprocess_text(doc.job_description)
        
        resume_skills = extract_skills(processed_resume)
        jd_skills = extract_skills(processed_jd)

        # Milestone 3 - Phase 1: Similarity Calculation
        vectors, _ = generate_tfidf_vectors(processed_resume, processed_jd)
        match_score = calculate_match_score(vectors)

        # Milestone 3 - Phase 2 & 3: Skill Gap & Taxonomy
        missing_skills = identify_skill_gap(resume_skills, jd_skills)
        grouped_missing = group_skills_by_category(missing_skills, skill_taxonomy)

        # Milestone 4 - Step 13: Skill Suggestion Engine
        suggestions = suggestion_engine.get_all_suggestions(jd_skills, resume_skills)

        analysis_result = {
            "match_percentage": match_score,
            "matched_skills": resume_skills,
            "missing_skills": missing_skills,
            "gap_analysis": grouped_missing,
            "suggestions": suggestions
        }

        docs_col.insert_one({
            "user_email": current_user,
            "resume_text": doc.resume_text,
            "job_description": doc.job_description,
            
            # Store NLP Results
            "processed_resume": processed_resume,
            "processed_jd": processed_jd,
            **analysis_result,
            
            "created_at": datetime.utcnow(),
            "timestamp": datetime.utcnow()
        })

        update_stats(resume_skills + jd_skills)
        
        return analysis_result

    except Exception as e:
        print(f"Analysis Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Neural Analysis Failed: {str(e)}"
        )


@router.get("/history", response_model=List[dict])
def get_history(current_user: str = Depends(get_current_user)):
    docs = list(docs_col.find({"user_email": current_user}))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs

@router.delete("/{doc_id}")
def delete_document(doc_id: str, current_user: str = Depends(get_current_user)):
    from bson import ObjectId
    result = docs_col.delete_one({"_id": ObjectId(doc_id), "user_email": current_user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Deleted successfully"}

@router.get("/stats")
def get_stats():
    from backend.database import get_user_collection
    users_col = get_user_collection()
    return {
        "total_users": users_col.count_documents({}),
        "total_documents": docs_col.count_documents({})
    }

@router.get("/skills")
def get_skills():
    # In a real app, this would fetch from a database collection of global skills
    # For now, we return the taxonomy keys as a proxy
    return {"skills": list(skill_taxonomy.keys())}

@router.post("/skills")
def add_skill(data: dict):
    # Simplified placeholder for adding to global skills
    return {"message": f"Skill {data.get('skill')} added to queue"}
