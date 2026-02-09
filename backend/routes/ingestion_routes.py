from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from backend.database import get_database
from backend.models import IngestionCreate
from backend.utils.text_extraction import extract_text_from_file
from backend.auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
db = get_database()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = await db.users.find_one({"email": email})
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

@router.post("/ingest")
async def ingest_data(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    data_type: str = Form(...), # 'resume' or 'jd'
    current_user: dict = Depends(get_current_user)
):
    content = ""
    filename = None
    
    if file:
        file_bytes = await file.read()
        filename = file.filename
        content = extract_text_from_file(file_bytes, filename)
    elif text:
        content = text
    else:
        raise HTTPException(status_code=400, detail="No file or text provided")
    
    ingestion_data = {
        "user_id": str(current_user["_id"]),
        "type": data_type,
        "content": content,
        "filename": filename,
        "timestamp": IngestionCreate.model_fields['timestamp'].default_factory()
    }
    
    await db.ingestions.insert_one(ingestion_data)
    
    return {"message": f"{data_type.capitalize()} ingested successfully", "content": content}

@router.get("/latest/{data_type}")
async def get_latest_ingestion(
    data_type: str,
    current_user: dict = Depends(get_current_user)
):
    ingestion = await db.ingestions.find_one(
        {"user_id": str(current_user["_id"]), "type": data_type},
        sort=[("timestamp", -1)]
    )
    if not ingestion:
        return {"content": None}
    
    return {
        "content": ingestion["content"],
        "filename": ingestion.get("filename"),
        "timestamp": ingestion["timestamp"].isoformat() if ingestion.get("timestamp") else None
    }
