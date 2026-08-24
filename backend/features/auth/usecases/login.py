from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.repository import UserRepository
from backend.features.auth.schema import LoginRequest, TokenResponse


async def user_login(data :LoginRequest, db: AsyncSession) -> TokenResponse:
    user_email = data.user_email
    user_password = data.user_password
    user = await UserRepository.get_user_by_email(user_email, db)