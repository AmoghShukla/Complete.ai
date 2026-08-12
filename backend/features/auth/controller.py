from fastapi import APIRouter, status, Depends
from .schema import SignupReponse, SignupRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])

