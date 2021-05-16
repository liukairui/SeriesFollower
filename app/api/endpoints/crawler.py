from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.endpoints.utils.crawler import update_common_task, update_detail_task
from app.api.endpoints.utils.db import get_db
from app.crawler import iqiyi, youku, tencent
from app.crud import crud_crawler
from app.schemas.album import AlbumPopularRead

router = APIRouter()

crawler_list = [iqiyi, youku, tencent]


# 获取热门
@router.get('/get_popular', response_model=List[List[AlbumPopularRead]])
def get_popular(db: Session = Depends(get_db)):
    result = crud_crawler.get_popular(db=db)
    return result


# 更新热门
@router.get('/update_popular')
def update_popular(db: Session = Depends(get_db)):
    crud_crawler.clear_popular(db=db)
    for index, crawler in enumerate(crawler_list):
        aid_list = []
        sid = index + 1
        popular_list = crawler.common(1)
        for i in range(10):
            aid_list.append(popular_list[i]['aid'])
        print(aid_list)
        crud_crawler.update_popular(sid=sid, aid_list=aid_list, db=db)
    return {'message': '热门条目已更新'}


# 更新爱奇艺剧集信息
@router.get('/update_iqiyi_common')
def update_iqiyi_common(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_common_task, 1, db)
    return {'message': 'iqiyi 基础数据后台更新中...'}


# 更新优酷剧集信息
@router.get('/update_youku_common')
def update_youku_common(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_common_task, 2, db)
    return {'message': 'youku 基础数据后台更新中...'}


# 更新腾讯剧集信息
@router.get('/update_tencent_common')
def update_tencent_common(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_common_task, 3, db)
    return {'message': 'tencent 基础数据后台更新中...'}


# 更新全部平台剧集信息
@router.get('/update_all_common')
def update_all_common(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_common_task, 1, db)
    background_task.add_task(update_common_task, 2, db)
    background_task.add_task(update_common_task, 3, db)
    return {'message': '全平台基础数据后台更新中...'}


# 更新爱奇艺详细剧集信息
@router.get('/update_iqiyi_detail')
def update_iqiyi_detail(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_detail_task, 1, db)
    return {'message': 'iqiyi 详细数据后台更新中...'}


# 更新优酷详细剧集信息
@router.get('/update_youku_detail')
def update_youku_detail(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_detail_task, 2, db)
    return {'message': 'youku 详细数据后台更新中...'}


# 更新腾讯详细剧集信息
@router.get('/update_tencent_detail')
def update_tencent_detail(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_detail_task, 3, db)
    return {'message': 'tencent 详细数据后台更新中...'}


# 更新全部平台详细剧集信息
@router.get('/update_all_detail')
def update_all_common(background_task: BackgroundTasks, db: Session = Depends(get_db)):
    background_task.add_task(update_detail_task, 1, db)
    background_task.add_task(update_detail_task, 2, db)
    background_task.add_task(update_detail_task, 3, db)
    return {'message': '全平台基础数据后台更新中...'}
