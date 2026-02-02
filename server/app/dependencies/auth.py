from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from app.models.user import User
import os

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    credentials = token.credentials
    try:
        payload = jwt.decode(credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user = await User.get(payload["id"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
