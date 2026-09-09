from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.session import get_db
from backend.features.auth.repository import UserRepository
from backend.models.user import User
from backend.utilities.exceptions import BadRequestException, UnauthorizedException
from backend.utilities.security import Security


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Bearer access token required")

    try:
        payload = Security.decode_token(
            credentials.credentials,
            expected_type="access",
        )
        user_id = UUID(payload["sub"])
    except (BadRequestException, ValueError, TypeError, KeyError) as exc:
        raise UnauthorizedException("Invalid or expired access token") from exc

    user = await UserRepository.get_user_by_id(user_id, db)
    if user is None:
        raise UnauthorizedException("User not found")

    return user