from fastapi import APIRouter
from pydantic import BaseModel
from app.core.gemini_chat import chat_with_gemini 

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/")
def chat(request: ChatRequest):
    reply = chat_with_gemini(request.message) 
    return {"reply": reply}
