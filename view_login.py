import streamlit as st
st.set_page_config(page_title="Đăng nhập", layout="centered")
import requests
from streamlit_cookies_manager import EncryptedCookieManager

st.title("🔐 Đăng nhập / Đăng ký")

API_BASE = "http://localhost:8000"

# Ẩn sidebar mặc định
st.markdown("""
    <style>
    [data-testid="stSidebarNav"], [data-testid="stSidebarNav"] + div {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Khởi tạo cookie ---
cookies = EncryptedCookieManager(prefix="myapp_", password="your-secret-key")
if not cookies.ready():
    st.stop()

# Nếu đã có token thì chuyển trang chat
if cookies.get("token"):
    st.switch_page("pages/view_chat.py")

# --- ĐĂNG KÝ ---
with st.expander("Bạn chưa có tài khoản? 👉 Đăng ký tại đây"):
    reg_name = st.text_input("Tên", key="reg_name")
    reg_email = st.text_input("Email đăng ký", key="reg_email")
    reg_password = st.text_input("Mật khẩu", type="password", key="reg_password")
    if st.button("Đăng ký"):
        res = requests.post(f"{API_BASE}/register/", json={
            "name": reg_name,
            "email": reg_email,
            "password": reg_password
        })
        if res.status_code == 200:
            st.success("🎉 Đăng ký thành công!")
        else:
            st.error(f"❌ {res.json()}")

# --- ĐĂNG NHẬP ---
st.subheader("🔑 Đăng nhập")
login_email = st.text_input("Email", key="login_email")
login_password = st.text_input("Mật khẩu", type="password", key="login_password")
if st.button("Đăng nhập"):
    form_data = {
        "username": login_email,
        "password": login_password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(f"{API_BASE}/login/", data=form_data, headers=headers)
    if res.status_code == 200:
        token = res.json()["access_token"]
        cookies["token"] = token
        cookies.save()
        st.success("✅ Đăng nhập thành công! Đang chuyển hướng...")
        st.rerun()
    else:
        st.error("❌ Sai tài khoản hoặc mật khẩu")
