from fastapi import APIRouter, status, Depends
from .schema import SignupReponse, SignupRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await user_signup(data, db)

@router.post(prefix='/login', status_code=status.HTTP_200_OK)
