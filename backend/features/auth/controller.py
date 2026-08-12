from fastapi import APIRouter, status, Depends
from .schema import SignupReponse, SignupRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
