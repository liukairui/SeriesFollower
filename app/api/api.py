from fastapi import APIRouter

from app.api.endpoints import login, album, crawler, follow, admin

api_router = APIRouter()
api_router.include_router(login.router, prefix='/login', tags=['登录模块'])
api_router.include_router(album.router, prefix='/album', tags=['剧集模块'])
api_router.include_router(crawler.router, prefix='/crawler', tags=['爬虫模块'])
api_router.include_router(follow.router, prefix='/follow', tags=['关注模块'])
api_router.include_router(admin.router, prefix='/admin', tags=['后台管理'])
