import streamlit as st
st.set_page_config(page_title="Chat với AI", layout="centered")
import requests
from streamlit_cookies_manager import EncryptedCookieManager

st.title("💬 Chatbot")

API_BASE = "http://localhost:8000"

# Ẩn sidebar mặc định
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebarNav"] + div {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Cookie chứa token đăng nhập
cookies = EncryptedCookieManager(prefix="myapp_", password="your-secret-key")
if not cookies.ready():
    st.stop()

if not cookies.get("token"):
    st.warning("🔐 Bạn chưa đăng nhập.")
    st.switch_page("view_login.py")

token = cookies["token"]

# Nút đăng xuất
if st.button("🚪 Đăng xuất"):
    cookies["token"] = ""
    cookies.save()
    st.success("Đã đăng xuất!")
    st.rerun()

# Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị đoạn chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Người dùng gửi tin nhắn
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi câu hỏi tới backend
    res = requests.post(
        f"{API_BASE}/chat/",
        json={"message": prompt},
        headers={"Authorization": f"Bearer {token}"}
    )

    if res.status_code == 200:
        reply = res.json()["reply"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    else:
        st.error("❌ Token hết hạn hoặc không hợp lệ.")
