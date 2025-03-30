from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, database
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

# Khởi tạo FastAPI
app = FastAPI()

# Khởi tạo database
models.Base.metadata.create_all(bind=database.engine)

# Test
@app.get("/ping")
def ping():
    return {"message": "pong"}

# CREATE /users
@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra user đã tồn tại
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
