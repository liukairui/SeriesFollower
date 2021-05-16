import time
from multiprocessing import Pool

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.crawler import iqiyi, youku, tencent
from app.crud import crud_crawler, crud_album
from app.db.session import db_session
from app.schemas.album import AlbumCommonCreate

crawler = APIRouter()
site_list = ['iqiyi', 'youku', 'tencent']
crawler_list = [iqiyi, youku, tencent]


# 创建剧集任务
def create_album_task(album_list: list, db: Session):
    print('albums creating...')
    created = 0
    for album in album_list:
        crud_crawler.create_album(db=db, album=AlbumCommonCreate(**album))
    print(f'{created} albums created')


# 更新剧集基本信息任务
def update_common_task(site: int, db: Session):
    print(f'[{site_list[site - 1]}]\ncommon info updating...')
    start_time = time.time()
    album_list = crawler_list[site - 1].crawl_common()
    created = 0
    updated = 0
    for album in album_list:
        album = AlbumCommonCreate(**album)
        res = crud_crawler.update_album(db=db, album=album)
        if res == 'created':
            created = created + 1
        elif res == 'updated':
            updated = updated + 1
    print(f'{created} created, {updated} updated in {round(time.time() - start_time, 2)} seconds')


# 爬取详情页并写入数据库
def crawl_and_create(db_data):
    if db_data.desc != 'null':
        return False
    if db_data.play_url == '':
        return False
    site = db_data.sid
    while True:
        detail = crawler_list[site - 1].crawl_detail(db_data)
        if detail:
            break
    db = db_session()
    crud_crawler.create_detail(
        db=db,
        detail={'aid': detail['aid'], 'desc': detail['desc']},
        director=detail['director'],
        actor=detail['actor']
    )
    db.close()
    return True


# 更新剧集详细信息任务
def update_detail_task(site: int, db: Session):
    print(f'[{site_list[site - 1]}]\ndetail info updating...')
    start_time = time.time()

    # 将指定 sid 的数据获取之后作为迭代器参数送入多线程池
    db_data = crud_album.get_album_by_site(db=db, site=site)
    pool = Pool(processes=16)
    updated = 0
    result = pool.map_async(crawl_and_create, db_data).get()
    for i in result:
        if i:
            updated = updated + 1
    pool.close()
    pool.join()

    print(f'{site_list[site - 1]} detail info {updated} updated in {round(time.time() - start_time, 2)} seconds')
