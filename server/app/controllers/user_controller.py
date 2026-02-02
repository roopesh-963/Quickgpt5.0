from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.user import User
from app.dependencies.auth import get_current_user
import bcrypt, jwt, os
from datetime import datetime
from passlib.context import CryptContext


router = APIRouter()

# Pydantic schemas
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
# JWT helper
def generate_token(user_id: str):
    return jwt.encode({"id": user_id}, os.getenv("JWT_SECRET"), algorithm="HS256")

# REGISTER
@router.post("/register")
async def register_user(req: RegisterRequest):
    existing = await User.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt())
    user = User(name=req.name, email=req.email, password=hashed.decode())
    await user.insert()
    token = generate_token(str(user.id))
    return {"success": True, "token": token, "user": {"id": str(user.id), "name": user.name, "email": user.email, "credits": user.credits}}

# LOGIN
@router.post("/login")
async def login_user(req: LoginRequest):
    user = await User.find_one({"email": req.email})
    if not user or not bcrypt.checkpw(req.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = generate_token(str(user.id))
    return {"success": True, "token": token}

# GET CURRENT USER
@router.get("/data")
async def get_user(current_user: User = Depends(get_current_user)):
    return {"success": True, "user": {"id": str(current_user.id), "name": current_user.name, "email": current_user.email, "credits": current_user.credits}}
