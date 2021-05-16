import re
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from fake_useragent import UserAgent

ua = UserAgent()


# 获取总页数
def get_total_page(start_page):
    current_page = start_page
    while True:
        # request 获取网页源代码
        url = f'https://list.iqiyi.com/www/2/-------------24-{current_page}-1-iqiyi--.html'
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0)'}

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        # 若找到最后一页的特殊元素，则跳出循环，返回当前页码
        if soup.find(attrs={'data-id': 'next'}, class_='page a1 noPage'):
            break
        else:
            current_page = current_page + 1
    return current_page


# 爬取基本信息
def common(current_page):
    # 循环访问直到获取到数据，避免某些时刻 JS 加载过慢导致获取不到数据
    while True:
        # request 获取网页源代码
        url = f'https://list.iqiyi.com/www/2/-------------11-{current_page}-1-iqiyi--.html'
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0)'}

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        item_list = soup.find_all(class_='qy-list-img')
        if item_list:
            break

    # 爬取对应字段，构建结果对象
    data = []
    for item in item_list:
        sid = 1
        aid = item.a['data-album-id']
        title = item.a['title']
        status = item.find(class_='qy-mod-label').string
        latest_ep = int(re.search(r'\d+', status)[0])
        is_finished = 1 if re.search(r'全', status) else 0
        cover_url = 'https:' + item.a.img['src']
        play_url = 'https:' + item.a['href']
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
    # 统计运行时间，获取页码
    start_time = time.time()
    total_page = get_total_page(start_page=18)

    # 配置多线程
    pool = Pool(processes=16)
    result = pool.map_async(common, range(1, total_page + 1)).get()
    pool.close()
    pool.join()

    # 处理数据
    album_list = []
    for i in result:
        for j in i:
            if j not in album_list:
                album_list.append(j)

    # 输出统计信息
    print(f'{total_page} pages, {len(album_list)} results in {round(time.time() - start_time, 2)} seconds')

    # 返回包含所有结果的数组
    return album_list


def crawl_detail(data):
    url = data.play_url
    headers = {'User-Agent': ua.random}

    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    aid = data.id

    desc = soup.find(class_='content-paragraph')
    if desc is None or desc.string is None:
        desc = '暂无简介'
    else:
        desc = desc.string
        if len(desc) > 500:
            desc = desc[0:500]

    director = []
    for i in soup.find_all('a', attrs={'itemprop': 'director'}):
        director.append(i.string)

    actor = []
    for i in soup.find_all('a', attrs={'itemprop': 'actor'}):
        actor.append(i.string)

    res = {
        'aid': aid,
        'desc': desc,
        'director': director,
        'actor': actor
    }

    if desc == '暂无简介' and director == [] and actor == []:
        return None
    return res
