from sqlalchemy.orm import Session

from app.db.models import Album, Actor, Director


# 通过 sid 获取剧集
def get_album_by_site(site: int, db: Session):
    return db.query(Album).filter(Album.sid == site).all()


# 通过 title 获取剧集
def get_album_by_title(title: str, db: Session):
    return db.query(Album).filter(Album.title.like(f'%{title}%')).limit(50).all()


# 通过 actor 获取剧集
def get_album_by_actor(actor: str, db: Session):
    actor = db.query(Actor).filter(Actor.name == actor).first()
    if actor:
        return actor.album
    return None


# 通过 director 获取剧集
def get_album_by_director(director: str, db: Session):
    director = db.query(Director).filter(Director.name == director).first()
    if director:
        return director.album
    return None


# 通过 title 获取剧集详情
def get_album_detail_by_title(title: str, db: Session):
    return db.query(Album).filter(Album.title == title).all()
