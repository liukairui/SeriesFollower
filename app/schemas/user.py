from typing import Optional

from pydantic import BaseModel


class WxUserInfo(BaseModel):
    nickName: str
    gender: int
    language: str
    city: str
    province: str
    country: str
    avatarUrl: str


class UserBase(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserRead(UserBase):
    nickname: str


class UserCreate(UserBase):
    oid: str
    nickname: str


class UserUpdate(UserCreate):
    pass
