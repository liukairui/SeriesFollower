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
        url = f'https://www.youku.com/category/show/c_97_s_1_p_{current_page}.html'
        headers = {'User-Agent': ua.chrome}

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        # 若找到最后一页的特殊元素，则跳出循环，返回当前页码
        if soup.find(class_='null-seek'):
            break
        else:
            current_page = current_page + 1
    return current_page


# 爬取基本信息
def common(current_page):
    # request参数
    url = f'https://www.youku.com/category/show/c_97_s_1_p_{current_page}.html'
    headers = {'User-Agent': ua.chrome}

    # 请求页面源代码
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    # 爬取对应字段，构建结果对象
    data = []
    item_list = soup.find_all('div', class_='g-col')
    for item in item_list:
        sid = 2
        aid = re.search('id_(.+).html', item.find(class_='categorypack_pack_cover').a['href']).group(1)
        title = item.find(class_='categorypack_pack_cover').a['title']
        status = item.find(class_='categorypack_p_rb').span.string
        latest_ep = int(re.search(r'\d+', status)[0])
        is_finished = 1 if re.search(r'全', status) else 0
        cover_url = 'https:' + item.find(class_='categorypack_pack_cover').img['src']
        play_url = 'https:' + item.find(class_='categorypack_pack_cover').a['href']
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
    total_page = get_total_page(start_page=15)

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
    headers = {'User-Agent': ua.random, 'Connection': 'close'}

    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'

    string = r.text
    pattern = re.compile(r'"desc":"(.*?)"}')
    desc = pattern.search(string)
    if desc:
        desc = desc.group(1)
        if len(desc) > 500:
            desc = desc[0:500]
    else:
        desc = '暂无简介'

    aid = data.id

    director = []
    pattern_director = re.compile(r',"title":"([^"]*?)","isAliStar":false,"subtitleType":"GENERAL","subtitle":"导演"')
    result_director = pattern_director.findall(string)
    for i in result_director:
        if i not in director:
            director.append(i)

    actor = []
    pattern_actor = re.compile(r',"title":"([^"]*?)","isAliStar":false,"subtitleType":"GENERAL","subtitle":"饰')
    result_actor = pattern_actor.findall(string)
    for i in result_actor:
        if i not in actor:
            actor.append(i)

    res = {
        'aid': aid,
        'desc': desc,
        'director': director,
        'actor': actor
    }

    if desc == '暂无简介' and director == [] and actor == []:
        return None
    return res
