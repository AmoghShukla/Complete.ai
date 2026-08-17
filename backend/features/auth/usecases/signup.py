

from sqlalchemy.ext.asyncio import AsyncSession
from backend.features.auth.schema import SignupRequest


async def signup(data : SignupRequest, db :AsyncSession):
