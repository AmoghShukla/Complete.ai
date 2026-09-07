from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from backend.core.config import settings
from backend.utilities.exceptions import BadRequestException



password_context : PasswordHash = PasswordHash.recommended()

class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        try:
            return password_context.hash(password)
        except Exception as exc:
            raise BadRequestException("Error while hashing the password") from exc

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return password_context.verify(plain_password, hashed_password)
        except Exception as exc:
            raise BadRequestException("Error while verifying the password") from exc

    @staticmethod
    def _jwt_secret() -> str:
        if not settings.JWT_SECRET_KEY:
            raise BadRequestException("JWT_SECRET_KEY is not configured")
        return settings.JWT_SECRET_KEY

    @staticmethod
    def create_access_token(subject: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"sub": subject, "type": "access", "exp": expires_at}
        return jwt.encode(
            payload,
            Security._jwt_secret(),
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(subject: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        payload = {"sub": subject, "type": "refresh", "exp": expires_at}
        return jwt.encode(
            payload,
            Security._jwt_secret(),
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode_token(token: str, expected_type: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                Security._jwt_secret(),
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.InvalidTokenError as exc:
            raise BadRequestException("Invalid or expired token") from exc

        if payload.get("type") != expected_type or not payload.get("sub"):
            raise BadRequestException("Invalid token type")
        return payload