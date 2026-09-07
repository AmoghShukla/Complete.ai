from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.repository import UserRepository
from backend.features.auth.schema import LoginRequest, TokenResponse
from backend.utilities.exceptions import UnauthorizedException
from backend.utilities.security import Security


async def user_login(data :LoginRequest, db: AsyncSession) -> TokenResponse:
    user_email = data.user_email
    user_password = data.user_password
    user = await UserRepository.get_user_by_email(user_email, db)
    if not user or not Security.verify_password(user_password, user.user_password):
        raise UnauthorizedException("Invalid email or password")

    return TokenResponse(
        access_token=Security.create_access_token(str(user.user_id)),
        refresh_token=Security.create_refresh_token(str(user.user_id)),
    )