from sqlalchemy.orm import Session

from app.db.models import Album, Director, Actor
from app.schemas.album import AlbumCommonCreate


# 获取热门
def get_popular(db: Session):
    res = []
    for i in range(1, 4):
        site = db.query(Album).filter(Album.is_popular == 1).filter(Album.sid == i).all()
        if site:
            res.append(site)
    return res


# 清空热门

def clear_popular(db: Session):
    db.query(Album).filter(Album.is_popular == 1).update({'is_popular': 0})
    print('popular cleared')


# 更新热门
def update_popular(sid: int, aid_list: list, db: Session):
    for aid in aid_list:
        popular = db.query(Album).filter(Album.sid == sid).filter(Album.aid == aid).one()
        if popular:
            popular.is_popular = 1
            db.add(popular)
            db.commit()


# 创建剧集
def create_album(album: AlbumCommonCreate, db: Session):
    db_album = Album(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


# 更新剧集
def update_album(album: AlbumCommonCreate, db: Session):
    new_album = Album(**album.dict())
    db_album = db.query(Album).filter(Album.sid == new_album.sid).filter(Album.play_url == new_album.play_url)
    # 若数据库无数据则创建
    if not db_album.first():
        if create_album(db=db, album=album):
            return 'created'
    # 若找到则判断数据库数据与传入的数据的 latest_ep 是否相同，若不同则更新
    elif db_album.filter(Album.latest_ep != new_album.latest_ep).first():
        db_album.update({
            Album.latest_ep: new_album.latest_ep,
            Album.is_finished: new_album.is_finished
        })
        db.commit()
        return 'updated'
    return


# 创建剧集详情（简介、演员、导演）
def create_detail(detail: dict, director: list, actor: list, db: Session):
    album = db.query(Album).filter(Album.id == detail['aid']).first()
    album.desc = detail['desc']
    db.commit()

    for new_director in director:
        db_director = db.query(Director).filter(Director.name == new_director).first()
        if not db_director:
            db.add(Director(name=new_director))
            db.commit()
            db_director = db.query(Director).filter(Director.name == new_director).first()
        album.director.append(db_director)
        db.commit()

    for new_actor in actor:
        db_actor = db.query(Actor).filter(Actor.name == new_actor).first()
        if not db_actor:
            db.add(Actor(name=new_actor))
            db.commit()
            db_actor = db.query(Actor).filter(Actor.name == new_actor).first()
        album.actor.append(db_actor)
        db.commit()
