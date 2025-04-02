from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, database
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.routers import auth
from app.core.security import verify_password, create_access_token
from app.routers import protected

# Khởi tạo FastAPI
app = FastAPI()

app.include_router(auth.router)
app.include_router(protected.router)

# Khởi tạo database
models.Base.metadata.create_all(bind=database.engine)

# Test
@app.get("/ping")
def ping():
    return {"message": "pong"}

# CREATE /users
@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully!", "user_id": new_user.id}

# GET /users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.__dict__ for user in users]

# DELETE /users/<user_id>
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}

# Pydantic model cho update user
class UserUpdate(BaseModel):
    name: str
    email: str

# PUT /users/<user_id>
@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.email = user_data.email
    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully!", "user_id": user.id}

# Đăng nhập (login)
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
