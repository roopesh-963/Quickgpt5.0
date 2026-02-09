from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.user import User
from app.models.chat import Chat
from app.models.transaction import Transaction

from app.config import init_db

from app.controllers import user_controller, chat_controller, message_controller, credit_controller


app = FastAPI()

@app.on_event("startup")
async def startup_db():
    await init_db([User, Chat, Transaction])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
app.include_router(chat_controller.router, prefix="/api/chat", tags=["Chat"])
app.include_router(message_controller.router, prefix="/api/message", tags=["Message"])
app.include_router(credit_controller.router, prefix="/api/credit", tags=["Credit"])

@app.get("/")
async def root():
    return {"message": "Server is live!"}
