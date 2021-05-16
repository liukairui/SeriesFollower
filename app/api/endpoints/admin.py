from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.utils.db import get_db
from app.api.endpoints.utils.verify import get_current_user
from app.crud import crud_admin
from app.schemas.admin import SwitchAdmin, SwitchIsActive

router = APIRouter()


@router.post('/get_all_users')
def get_all_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='权限不足')
    return crud_admin.get_all_users(db=db)


@router.post('/switch_admin')
def switch_admin(sa: SwitchAdmin, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='权限不足')
    return crud_admin.switch_admin(db=db, user_id=sa.user_id)


@router.post('/switch_is_active')
def switch_is_active(sa: SwitchIsActive, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='权限不足')
    return crud_admin.switch_is_active(db=db, user_id=sa.user_id)
