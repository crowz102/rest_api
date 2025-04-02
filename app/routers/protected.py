from fastapi import APIRouter, Security, HTTPException
from app.routers.auth import oauth2_scheme

router = APIRouter()

@router.get("/protected-route")
def protected_route(token: str = Security(oauth2_scheme)):
     if not token:
         raise HTTPException(status_code=401, detail="Invalid token")
     return {"message": "You have access a protected route", "token": token}