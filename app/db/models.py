from sqlalchemy import func, Column, SmallInteger, Integer, Boolean, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

# 剧集-演员关系表
album_actor = Table(
    'album_actor',
    Base.metadata,
    Column('album_id', Integer, ForeignKey('album.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
)
# 剧集-导演关系表
album_director = Table(
    'album_director',
    Base.metadata,
    Column('album_id', Integer, ForeignKey('album.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
)


# 视频表
class Site(Base):
    __tablename__ = 'site'
    id = Column(SmallInteger, primary_key=True, autoincrement=True, comment='平台ID')
    name = Column(String(10), nullable=False, comment='平台名称')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    album = relationship('Album', back_populates='site')


# 演员表
class Actor(Base):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='演员ID')
    name = Column(String(50), nullable=False, comment='演员名')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    album = relationship('Album', secondary=album_actor, back_populates='actor')


# 导演表
class Director(Base):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='导演ID')
    name = Column(String(50), nullable=False, comment='导演名')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    album = relationship('Album', secondary=album_director, back_populates='director')


# 剧集表
class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    sid = Column(SmallInteger, ForeignKey('site.id'), comment='平台ID')
    aid = Column(String(30), nullable=False, comment='平台各自定义的剧集ID')
    title = Column(String(50), nullable=False, comment='剧名')
    latest_ep = Column(SmallInteger, nullable=False, comment='最新集数')
    is_finished = Column(SmallInteger, nullable=False, comment='是否完结')
    cover_url = Column(String(500), nullable=False, comment='剧照地址')
    play_url = Column(String(500), nullable=False, comment='播放地址')
    desc = Column(String(2000), nullable=False, default='null', comment='简介')
    is_popular = Column(Integer, default=0, comment='是否热门')
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 视频平台对剧集：一对多
    site = relationship('Site', back_populates='album')
    # 剧集对演员：多对多
    actor = relationship('Actor', secondary=album_actor, back_populates='album')
    # 剧集对导演：多对多
    director = relationship('Director', secondary=album_director, back_populates='album')
    # 订阅关系（用户对剧集：多对多）
    user = relationship('UserAlbum', back_populates='album')


# 用户表
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    oid = Column(String(30), nullable=False, comment='OpenID')
    nickname = Column(String(30), nullable=False, comment='昵称')
    is_active = Column(Boolean(), nullable=False, default=True, comment='是否激活')
    is_superuser = Column(Boolean(), nullable=False, default=False, comment='是否是超级用户')

    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    album = relationship('UserAlbum', back_populates='user')


# 用户-剧集关系表
class UserAlbum(Base):
    __tablename__ = 'user_album'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    user_id = Column(Integer, ForeignKey('user.id'), comment='用户ID')
    album_id = Column(Integer, ForeignKey('album.id'), comment='剧集ID')
    last_ep = Column(Integer, nullable=False, comment='用户上次点击时的集数')
    status = Column(Boolean, nullable=False, default=True, comment='有效状态')

    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    album = relationship('Album', back_populates='user')
    user = relationship('User', back_populates='album')
