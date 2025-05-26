from openai import OpenAIError, RateLimitError, OpenAI
from app.core.config import settings 

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def chat_with_openai(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        return "Bạn đã vượt quá giới hạn sử dụng API. Vui lòng kiểm tra quota hoặc thử lại sau."
    except OpenAIError as e:
        return f"Đã có lỗi xảy ra khi gọi API OpenAI: {e}"
