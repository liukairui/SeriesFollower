from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.endpoints.utils.db import get_db
from app.api.endpoints.utils.verify import get_current_user
from app.crud import crud_follow
from app.schemas.follow import ChangeFollowStatus

router = APIRouter()


@router.post('/get_follow_list')
def get_follow_list(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_follow.get_follow_list(user_id=user.id, db=db)


@router.post('/get_follow_list_detail')
def get_follow_list_detail(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_follow.get_follow_list_detail(user_id=user.id, db=db)


@router.post('/change_follow_status')
def change_follow(data: ChangeFollowStatus, db: Session = Depends(get_db),
                  user=Depends(get_current_user)):
    return crud_follow.change_follow_status(user_id=user.id, album_id=data.album_id, last_ep=data.last_ep, db=db)


@router.post('/update_last_ep')
def update_last_ep(data: ChangeFollowStatus, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    return crud_follow.update_last_ep(user_id=user.id, album_id=data.album_id, last_ep=data.last_ep, db=db)
