from datetime import datetime

from pydantic import BaseModel


class AlbumCommonCreate(BaseModel):
    sid: int
    aid: str
    title: str
    latest_ep: int
    is_finished: int
    cover_url: str
    play_url: str


class AlbumCommonRead(AlbumCommonCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AlbumDetailCreate(BaseModel):
    aid: str
    desc: str


class AlbumDetailRead(AlbumDetailCreate):
    id: int
    sid: int
    title: str
    latest_ep: int
    is_finished: int
    cover_url: str
    play_url: str
    updated_at: datetime
    actor: list
    director: list

    class Config:
        orm_mode = True


class AlbumPopularRead(BaseModel):
    sid: int
    title: str
    latest_ep: int
    is_finished: int
    cover_url: str
    play_url: str
    is_popular: int

    class Config:
        orm_mode = True


class AlbumSearchResult(BaseModel):
    id: int
    sid: int
    title: str
    is_finished: int

    class Config:
        orm_mode = True
