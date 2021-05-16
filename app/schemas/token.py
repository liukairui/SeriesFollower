from app.schemas.user import UserRead
from pydantic import BaseModel


class Login(BaseModel):
    js_code: str
    user_info: dict


class Token(BaseModel):
    access_token: str
    token_type: str
    is_superuser: bool


class TokenPayload(BaseModel):
    openid: str
