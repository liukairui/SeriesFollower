from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import User
from app.api.endpoints.utils.db import get_db
from app.core import openid
from app.core.config import settings
from app.core.jwt import create_access_token
from app.crud import crud_user
from app.schemas.token import Login, Token
from app.schemas.user import WxUserInfo, UserCreate
from app.api.endpoints.utils.db import get_db
from app.api.endpoints.utils.verify import get_current_user

router = APIRouter()


@router.post('/', response_model=Token)
def login(data: Login, db: Session = Depends(get_db)):
    user_info = WxUserInfo(**data.user_info)
    oid = openid.get(data.js_code)
    user = crud_user.get_by_oid(db=db, oid=oid)
    # 若昵称不同则更新昵称
    if user and user.nickname != user_info.nickName:
        user.nickname = user_info.nickName
        db.commit()
    # 若未找到用户则创建
    if not user:
        user = crud_user.create(db=db, obj_input=UserCreate(oid=oid, nickname=user_info.nickName))
        print(f'user {user.oid} created')
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='未激活用户'
        )
    print(f'user {user.oid} logged in')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': create_access_token(data={'openid': oid}, expires_delta=access_token_expires),
        'token_type': 'bearer',
        'is_superuser': user.is_superuser
    }


@router.post('/deactivate')
def deactivate(user=Depends(get_current_user), db: Session = Depends(get_db)):
    crud_user.deactivate(db=db, user_id=user.id)
