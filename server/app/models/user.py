from beanie import Document
from pydantic import EmailStr
from typing import Optional


class User(Document):
    name: str
    email: EmailStr
    password: str
    credits: int = 20

    class Settings:
        name = "users"
