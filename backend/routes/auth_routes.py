from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from backend.database import get_database
from backend.models import UserCreate, UserInDB, Token
from backend.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
db = get_database()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    try:
        user_exists = await db.users.find_one({"email": user.email})
        if user_exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)
        new_user = {"email": user.email, "hashed_password": hashed_password}
        await db.users.insert_one(new_user)
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await db.users.find_one({"email": form_data.username})
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        access_token = create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
