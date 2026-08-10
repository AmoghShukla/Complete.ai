from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=255)
    user_email: EmailStr
    user_password: str = Field(..., min_length=8)

class SignupReponse(BaseModel):
    user_id : UUID
    user_name : str
    role : str
    user_email : str

class LoginRequest(BaseModel):
    user_email: EmailStr
    user_password: str

class TokenResponse(BaseModel):
    access_token : str
    refresh_token : str
