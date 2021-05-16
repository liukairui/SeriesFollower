from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_by_oid(db: Session, oid: str):
    return db.query(User).filter(User.oid == oid).first()


def create(db: Session, obj_input: UserCreate):
    db_obj = User(
        oid=obj_input.oid,
        nickname=obj_input.nickname,
        is_active=obj_input.is_active,
        is_superuser=obj_input.is_superuser
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, obj_input: UserUpdate):
    db_obj: User = get_by_oid(db, obj_input.oid)
    db_obj.is_active = obj_input.is_active
    db_obj.is_superuser = obj_input.is_superuser
    db.commit()
    return db_obj


def deactivate(db: Session, user_id: int):
    db_user: User = db.query(User).filter(User.id == user_id).first()
    db_user.is_active = False
    db.commit()
