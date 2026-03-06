from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Request
from backend.models import DocumentResponse
from backend.database import get_document_collection

from nlp.preprocessing import preprocess_text
from nlp.skill_extractor import extract_skills
from nlp.vectorizer import generate_tfidf_vectors
from nlp.matcher import calculate_match_score, calculate_match_score_semantic, identify_skill_gap, group_skills_by_category
from nlp.suggestion_engine import SuggestionEngine
from nlp.file_processor import get_text_from_file
from app_data.skill_taxonomy import skill_taxonomy
from core.usage_stats import update_stats
from core.llm_service import narrative_service

from datetime import datetime
from typing import List, Any
from pydantic import BaseModel

router = APIRouter()
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

@router.post("/", response_model=Any)
async def upload_document(
    request: Request,
):
    print("CRITICAL_DEBUG: REACHED upload_document")
    print(f"DEBUG: Content-Type: {request.headers.get('content-type')}")
    
    # Manually parse form data to avoid Pydantic "Invalid body" for Multipart
    try:
        form = await request.form()
        resume_file = form.get('resume_file')
        job_description = form.get('job_description')
    except Exception as e:
        print(f"DEBUG: Form Parsing Error: {str(e)}")
        # Check if it was sent as JSON instead by mistake
        try:
            json_data = await request.json()
            print(f"DEBUG: Received JSON instead: {json_data}")
            resume_file = json_data.get('resume_file')
            job_description = json_data.get('job_description')
        except:
            raise HTTPException(status_code=400, detail=f"Failed to parse request body: {str(e)}")

    # Mock user for debug
    current_user = "debug_user@example.com"
    
    docs_col = get_document_collection()
    if docs_col is None:
        raise HTTPException(status_code=503, detail="Database connection failed.")

    if not resume_file or not job_description:
        raise HTTPException(status_code=400, detail="Missing resume_file or job_description")

    try:
        # Step 1: Extract Text from File
        resume_content = await resume_file.read()
        resume_text = get_text_from_file(resume_content, resume_file.filename)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the provided file.")

        # Step 2: NLP Pipeline
        processed_resume = preprocess_text(resume_text)
        processed_jd = preprocess_text(job_description)
        
        resume_skills = extract_skills(processed_resume)
        jd_skills = extract_skills(processed_jd)

        # Step 3: Semantic & TF-IDF Matching
        # We use the new semantic score for the main result
        match_score = calculate_match_score_semantic(resume_text, job_description)
        
        # Keep TF-IDF for fallback/legacy or comparison if needed
        # vectors, _ = generate_tfidf_vectors(processed_resume, processed_jd)
        # tfidf_score = calculate_match_score(vectors)

        # Step 4: Gap Analysis
        missing_skills = identify_skill_gap(resume_skills, jd_skills)
        grouped_missing = group_skills_by_category(missing_skills, skill_taxonomy)

        # Step 5: Actionable Learning Roadmap
        learning_roadmap = suggestion_engine.get_actionable_roadmap(missing_skills)

        # Step 6: LLM Strategic Narrative (Gemini)
        insights = await narrative_service.generate_insights(resume_text, job_description, match_score, missing_skills)

        analysis_result = {
            "match_percentage": match_score,
            "matched_skills": resume_skills,
            "missing_skills": missing_skills,
            "gap_analysis": grouped_missing,
            "learning_roadmap": learning_roadmap,
            "insights": insights
        }

        docs_col.insert_one({
            "user_email": current_user,
            "resume_filename": resume_file.filename,
            "resume_text": resume_text,
            "job_description": job_description,
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
    docs_col = get_document_collection()
    if docs_col is None:
        raise HTTPException(status_code=503, detail="Database connection failed.")
        
    docs = list(docs_col.find({"user_email": current_user}))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs

@router.delete("/{doc_id}")
def delete_document(doc_id: str, current_user: str = Depends(get_current_user)):
    from bson import ObjectId
    docs_col = get_document_collection()
    if docs_col is None:
        raise HTTPException(status_code=503, detail="Database connection failed.")
        
    result = docs_col.delete_one({"_id": ObjectId(doc_id), "user_email": current_user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Deleted successfully"}

@router.get("/stats")
def get_stats():
    from backend.database import get_user_collection
    docs_col = get_document_collection()
    users_col = get_user_collection()
    if docs_col is None or users_col is None:
         return {"total_users": 0, "total_documents": 0, "status": "Database Offline"}
         
    return {
        "total_users": users_col.count_documents({}),
        "total_documents": docs_col.count_documents({})
    }

@router.get("/skills")
def get_skills():
    # In a real app, this would fetch from a database collection of global skills
    # For now, we return the taxonomy keys as a proxy
    return {"skills": list(skill_taxonomy.keys())}

from backend.models import SkillSchema

@router.post("/skills")
def add_skill(data: SkillSchema):
    # Simplified placeholder for adding to global skills
    return {"message": f"Skill {data.skill} added to queue"}
