from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user

router = APIRouter()

@router.get("/protected-route")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"You have access a protected route, user: {current_user}"}
