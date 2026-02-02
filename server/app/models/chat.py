from beanie import Document
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime
    is_image: bool = False
    is_published: bool = False

class Chat(Document):
    user_id: str
    name: str
    messages: List[Message] = []

    class Settings:
        name = "chats"
