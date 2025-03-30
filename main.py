from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

#Khoi tao FastAPI
app = FastAPI()

#Khoi tao database
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Test
@app.get("/ping")
def ping():
    return {"message": "pong"}

#CREATE /users
@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    if db_user:
        raise HTTPException(status_code=404, detail="User already exists")
    new_user = models.User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"User created successfully!", "user_id":new_user.id}

#GET /users
@app.get("/users/")
def get_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.__dict__ for user in users]

#DELETE /users/<user_id>
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    db.release(user)
    db.commit()

    return {"message":"User deleted successfully!"}

#PUT /users/<user_id>
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.name = name
    user.email = email
    db.commit()
    db.release(user)

    return {"message":"User updated successfully!", "user_id":user.id}

