import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from app.api.api import api_router
from app.core.config import settings
from app.db.session import db_session

app = FastAPI(
    title='追剧助手API接口文档',
    description='Series Follower API Docs',
    version='1.0.0',
    docs_url='/',
    redoc_url='/redocs'
)

app.include_router(api_router, prefix='/api')


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    中间件，在每次收到的 request 时，生成一个数据库会话并保存在 request.state 中，并确保在 response 前关闭
    """
    request.state.db = db_session()
    response = await call_next(request)
    request.state.db.close()
    return response


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD,
        debug=settings.UVICORN_DEBUG,
        workers=settings.UVICORN_WORKERS
    )
