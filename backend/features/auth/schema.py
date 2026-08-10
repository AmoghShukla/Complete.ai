from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=255)
    user_email: EmailStr
    user_password: str = Field(..., min_length=8)
