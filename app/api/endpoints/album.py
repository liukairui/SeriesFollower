from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.utils.db import get_db
from app.api.endpoints.utils.verify import get_current_user
from app.crud import crud_album
from app.schemas.album import AlbumSearchResult, AlbumDetailRead

router = APIRouter()


# 通过 title 搜索剧集
@router.get('/get_album_by_title', response_model=List[AlbumSearchResult], dependencies=[Depends(get_current_user)])
def get_album_by_title(title: str, db: Session = Depends(get_db)):
    return crud_album.get_album_by_title(title=title, db=db)


# 通过 actor 搜索剧集
@router.get('/get_album_by_actor', response_model=List[AlbumSearchResult],
            # dependencies=[Depends(get_current_user)]
            )
def get_album_by_actor(actor: str, db: Session = Depends(get_db)):
    return crud_album.get_album_by_actor(actor=actor, db=db)


# 通过 director 搜索剧集
@router.get('/get_album_by_director', response_model=List[AlbumSearchResult],
            # dependencies=[Depends(get_current_user)]
            )
def get_album_by_director(director: str, db: Session = Depends(get_db)):
    return crud_album.get_album_by_director(director=director, db=db)


# 通过 title 搜索剧集详情
@router.get('/get_album_detail_by_title', response_model=List[AlbumDetailRead],
            dependencies=[Depends(get_current_user)])
def get_album_detail_by_title(title: str, db: Session = Depends(get_db)):
    return crud_album.get_album_detail_by_title(title=title, db=db)
