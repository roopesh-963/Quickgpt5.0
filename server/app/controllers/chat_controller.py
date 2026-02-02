from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import Chat, Message
from app.dependencies.auth import get_current_user
from datetime import datetime
from pydantic import BaseModel


router = APIRouter()

# CREATE NEW CHAT
@router.post("/create")
async def create_chat(current_user = Depends(get_current_user)):
    chat = Chat(
        user_id=str(current_user.id),
        name="New Chat",
        messages=[],
    )
    await chat.insert()
    return {"success": True, "message": "Chat created", "chat_id": str(chat.id)}

# GET ALL CHATS
@router.get("/get")
async def get_chats(current_user = Depends(get_current_user)):
    chats = await Chat.find({"user_id": str(current_user.id)}).sort("-id").to_list()
    return {"success": True, "chats": chats}

# DELETE CHAT
class DeleteChatRequest(BaseModel):
    chat_id: str

@router.post("/delete")
async def delete_chat(req: DeleteChatRequest, current_user = Depends(get_current_user)):
    chat = await Chat.get(req.chat_id)
    if not chat or chat.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Chat not found")
    await chat.delete()
    return {"success": True, "message": "Chat deleted"}
