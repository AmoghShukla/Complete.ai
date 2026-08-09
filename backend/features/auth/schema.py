from pydantic import BaseModel, EmailStr

class Signup(BaseModel):
    user_name : str
    user_password : str