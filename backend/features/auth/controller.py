from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import SignupReponse, SignupRequest, LoginRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await user_signup(data, db)

@router.post(prefix='/login', status_code=status.HTTP_200_OK)
async def login(data : LoginRequest, db : AsyncSession = Depends(get_db)):
    return await user_login(data, db)