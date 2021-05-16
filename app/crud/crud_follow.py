from sqlalchemy.orm import Session

from app.db.models import User, UserAlbum, Album


def get_follow_list(db: Session, user_id: int):
    return db.query(UserAlbum).filter(UserAlbum.user_id == user_id).filter(UserAlbum.status).all()


def get_follow_list_detail(db: Session, user_id: int):
    user_album = db.query(UserAlbum).filter(UserAlbum.user_id == user_id).filter(UserAlbum.status).all()
    results = []
    for i in user_album:
        album = db.query(Album).filter(Album.id == i.album_id).first()
        results.append(album)
    return results


def change_follow_status(db: Session, user_id: int, album_id: int, last_ep: int):
    user = db.query(User).filter(User.id == user_id).first()
    for i in user.album:
        if i.album_id == album_id:
            i.status = not i.status
            i.last_ep = last_ep
            db.commit()
            return {'status': i.status}
    # 若数据库中没有关注信息
    album = db.query(Album).filter(Album.id == album_id).first()
    user_album = UserAlbum(
        last_ep=1
    )
    user_album.album = album
    user.album.append(user_album)
    db.commit()
    return {'status': True}


def update_last_ep(db: Session, user_id: int, album_id: int, last_ep: int):
    user_album = db.query(UserAlbum).filter(UserAlbum.user_id == user_id, UserAlbum.album_id == album_id).first()
    user_album.last_ep = last_ep
    db.commit()
