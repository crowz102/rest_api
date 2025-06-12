import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def chat_with_gemini(message: str) -> str:
    try:
        response = model.generate_content(message)
        return response.text.strip()
    except Exception as e:
        return f"Đã có lỗi xảy ra khi gọi Gemini API: {e}"
