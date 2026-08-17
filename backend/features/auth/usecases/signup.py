from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.repository import UserRepository
from backend.features.auth.schema import SignupRequest


async def signup(data : SignupRequest, db :AsyncSession):
    '''check whether the enetered email is unique or not'''
    user_exists = await UserRepository.get_user_by_email(data.user_email, db)
    if user_exists:
        raise ConflictException('Email Already Registered')
