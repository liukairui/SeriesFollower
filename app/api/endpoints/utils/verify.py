from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from jose.jwt import JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.api.endpoints.utils.db import get_db
from app.core.jwt import decode_access_token
from app.crud import crud_user


def get_current_user(db: Session = Depends(get_db), x_token: Optional[str] = Header(None)):
    if not x_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='未获取Token'
        )
    try:
        payload = decode_access_token(x_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Token过期或无效'
        )
    user = crud_user.get_by_oid(db=db, oid=payload.openid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到用户")
    return user

