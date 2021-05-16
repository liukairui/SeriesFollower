import re
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from fake_useragent import UserAgent

ua = UserAgent()


# 获取总页数
def get_total_page():
    url = f'https://v.qq.com/x/bu/pagesheet/list'
    headers = {'User-Agent': ua.chrome}
    payload = {
        '_all': 1,
        'append': 1,
        'channel': 'tv',
        'listpage': 2,
        'offset': 0,
        'pagesize': 30,
        'sort': 18
    }

    r = requests.get(url=url, headers=headers, params=payload)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    total_page = int(soup.find_all(class_='page_num')[-1].string)
    return total_page


# 爬取基本信息
def common(current_page):
    url = f'https://v.qq.com/x/bu/pagesheet/list'
    headers = {'User-Agent': ua.chrome}
    payload = {
        '_all': 1,
        'append': 1,
        'channel': 'tv',
        'listpage': 2,
        'offset': 30 * (current_page - 1),
        'pagesize': 30,
        'sort': 18
    }

    r = requests.get(url=url, headers=headers, params=payload)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    data = []
    item_list = soup.find_all('div', class_='list_item')
    for item in item_list:
        sid = 3
        aid = item.a['data-float']
        title = item.a['title']
        status = item.find(class_='figure_caption')
        if status is None:
            continue
        latest_ep = re.search(r'\d+', status.string)
        if latest_ep is None:
            continue
        latest_ep = int(latest_ep[0])
        is_finished = 1 if re.search(r'全', status.string) else 0
        cover_url = 'https:' + item.a.img['src']
        play_url = item.a['href']
        album = {
            'sid': sid,
            'aid': aid,
            'title': title,
            'latest_ep': latest_ep,
            'is_finished': is_finished,
            'cover_url': cover_url,
            'play_url': play_url
        }
        data.append(album)
    return data


def crawl_common():
    start_time = time.time()
    total_page = get_total_page()

    # 配置多线程
    pool = Pool(processes=16)
    result = pool.map_async(common, range(1, total_page + 1)).get()
    pool.close()
    pool.join()

    # 处理数据
    album_list = []
    for i in result:
        for j in i:
            if j and j not in album_list:
                album_list.append(j)

    # 输出统计信息
    print(f'{total_page} pages, {len(album_list)} results in {round(time.time() - start_time, 2)} seconds')

    # 返回包含所有结果的数组
    return album_list


def crawl_detail(data):
    url = data.play_url
    if url == '':
        return True
    headers = {'User-Agent': ua.random}

    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    aid = data.id

    desc = soup.find(class_='summary')
    if desc:
        desc = desc.string
        if len(desc) > 500:
            desc = desc[0:500]
    else:
        desc = '暂无简介'

    director = []
    actor = []

    director_actor = soup.find(class_='director')
    if director_actor:
        director_actor = director_actor.contents
        director_actor_str = ''
        for item in director_actor:
            director_actor_str = director_actor_str + str(item)
        director_actor_str_splited = director_actor_str.split('演员')

        director_str = ''
        actor_str = ''
        if len(director_actor_str_splited):
            director_str = director_actor_str_splited[0]
        if len(director_actor_str_splited) > 1:
            actor_str = director_actor_str_splited[1]
        s = BeautifulSoup(director_str, 'lxml').find_all('a')
        if s:
            for i in s:
                director.append(i.string)

        s = BeautifulSoup(actor_str, 'lxml').find_all('a')
        if s:
            for i in s:
                actor.append(i.string)

    res = {
        'aid': aid,
        'desc': desc,
        'director': director,
        'actor': actor
    }

    return res
