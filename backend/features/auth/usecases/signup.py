from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.repository import UserRepository
from backend.features.auth.schema import SignupRequest
from backend.models.user import User
from backend.utilities.exceptions import ConflictException
from backend.utilities.security import Security


async def signup(data : SignupRequest, db :AsyncSession):
    '''check whether the enetered email is unique or not'''
    user_exists = await UserRepository.get_user_by_email(data.user_email, db)
    if user_exists:
        raise ConflictException('Email Already Registered')
    new_user = User(
        user_name = data.user_name,
        user_email = data.user_email,
        user_password = Security.hash_password(data.user_password)
    )
    new_user = UserRepository.signup(new_user, db)
    
