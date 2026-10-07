from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.session import get_db

from .schema import (
    LoginRequest,
    RefreshTokenRequest,
    SignupRequest,
    SignupResponse,
    TokenResponse,
)
from .usecases.login import refresh_access_token, user_login
from .usecases.signup import Signup

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await Signup(data, db)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(data : LoginRequest, db : AsyncSession = Depends(get_db)):
    return await user_login(data, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshTokenRequest):
    return await refresh_access_token(data)