from sqlalchemy.orm import Session

from app.db.models import User


def get_all_users(db: Session):
    return db.query(User).all()


def switch_admin(db: Session, user_id: int):
    db_user: User = db.query(User).filter(User.id == user_id).first()
    db_user.is_superuser = not db_user.is_superuser
    db.commit()


def switch_is_active(db: Session, user_id: int):
    db_user: User = db.query(User).filter(User.id == user_id).first()
    db_user.is_active = not db_user.is_active
    db.commit()
