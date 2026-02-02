from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import Chat, Message
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.gemini_service import generate_text
from app.services.imagekit_service import upload_image
from datetime import datetime
import base64
from pydantic import BaseModel


router = APIRouter()

class TextMessageRequest(BaseModel):
    chat_id: str
    prompt: str

class ImageMessageRequest(BaseModel):
    chat_id: str
    prompt: str
    is_published: bool = False

# TEXT MESSAGE
@router.post("/text")
async def text_message(req: TextMessageRequest, current_user: User = Depends(get_current_user)):
    if current_user.credits < 1:
        raise HTTPException(status_code=403, detail="Not enough credits")

    chat = await Chat.get(req.chat_id)
    if not chat or chat.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Chat not found")

    # Add user message
    user_msg = Message(role="user", content=req.prompt, timestamp=datetime.utcnow(), is_image=False)
    chat.messages.append(user_msg)

    # Call Gemini AI
    try:
        ai_text = await generate_text(req.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    # Add AI reply
    reply = Message(role="assistant", content=ai_text, timestamp=datetime.utcnow(), is_image=False)
    chat.messages.append(reply)
    await chat.save()

    # Deduct 1 credit
    current_user.credits -= 1
    await current_user.save()

    return {"success": True, "reply": reply.dict()}

# IMAGE MESSAGE
@router.post("/image")
async def image_message(req: ImageMessageRequest, current_user: User = Depends(get_current_user)):
    if current_user.credits < 2:
        raise HTTPException(status_code=403, detail="Not enough credits")

    chat = await Chat.get(req.chat_id)
    if not chat or chat.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Chat not found")

    # Add user prompt
    user_msg = Message(role="user", content=req.prompt, timestamp=datetime.utcnow(), is_image=False)
    chat.messages.append(user_msg)

    # Generate "fake" AI image URL (simulate)
    encoded_prompt = base64.b64encode(req.prompt.encode()).decode()
    filename = f"{datetime.utcnow().timestamp()}.png"
    base64_file = f"data:image/png;base64,{encoded_prompt}"  # placeholder, in real you can generate AI image
    try:
        url = await upload_image(base64_file, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    reply = Message(role="assistant", content=url, timestamp=datetime.utcnow(), is_image=True, is_published=req.is_published)
    chat.messages.append(reply)
    await chat.save()

    # Deduct 2 credits
    current_user.credits -= 2
    await current_user.save()

    return {"success": True, "reply": reply.dict()}
