from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.schema import TokenResponse


async def user_login(data, db: AsyncSession) -> TokenResponse:
    user_email = data.username
    user_password = data.password
    user = await UserRepository.get_user_by_email(user_email, db)