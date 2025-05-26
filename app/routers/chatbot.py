from fastapi import APIRouter
from pydantic import BaseModel
from app.core.openai_chat import chat_with_openai

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/")
def chat(request: ChatRequest):
    reply = chat_with_openai(request.message)
    return {"reply": reply}
