from pydantic import BaseModel,EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    active: bool | None = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str| None ="Bearer"

class LoginSchema(BaseModel):
    password: str
    email: EmailStr

class TokenData(BaseModel):
    email: str | None = None