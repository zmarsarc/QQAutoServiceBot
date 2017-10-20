# -*- coding: utf-8 -*-

import requests
import bs4

modian_base_url = 'https://wds.modian.com'
items_main_page = '/show_weidashang_pro'
backer_list_api = '/ajax/backer_ranking_list'
fake_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/61.0.3163.100 Safari/537.36'
}
ckg_id = 8338
wds_header = u'金秋十月，碧空如洗，凉爽舒适。\
大家期待已久的snh48姐妹团——ckg48首演终于要来了！\
为了在首演更好地应援我们可爱的新成员，ckg应援会准备开设集资通道。\
所有集资所得的钱都将用于购买首演所需的应援物品。\
希望大家都能出点力，让成员看到我们的热情吧！\n\
为了庆祝CKG48 27号发布会\
应援会决定拿出两个观摩的名额作为集资奖励 \
*集资第一名即可获得 观摩名额一位\
*参与集资 20以上即可参与抽奖（抽观摩名额一位）\
此次集资不限所在地，全国聚聚都可以参与。\
如因故取消赠票资格，可全额退款，或经商议后转入应援会日常运营资金。\
出于丝芭长期运营风格的考虑，希望各位聚聚有以上心里准备。\
活动22号晚上11点截止\
微打赏链接：'


def auto_response(command):
    if 'wds' in command:
        return wds_header + modian_base_url + items_main_page + '/' + str(ckg_id)
    if 'rank' in command:
        ranks = rank(ckg_id)
        ret = u'集资排名 Top 10：\n'
        for i in range(10):
            ret += ranks[i] + '\n'
        ret += '感谢以上聚聚的大力支持，同时也感谢每位参与了集资的聚聚的无私奉献！'
        return ret
    else:
        return None


def rank(id):
    rank_url = modian_base_url + backer_list_api
    page = 1
    page_size = 20
    payload = {
        'pro_id': ckg_id,
        'type': 1,
        'page': page,
        'page_size': page_size
    }
    response = requests.post(rank_url, payload, headers=fake_header)

    if response.status_code != 200:
        return 'unexpected modian server error'

    json = response.json()
    ret = []
    while int(json['status']) != -1:
        ret.extend(format_html_record(json['data']['html']))
        payload['page'] += 1
        response = requests.post(rank_url, payload, headers=fake_header)
        json = response.json()

    return ret


def format_html_record(record):
    ret = []
    soup = bs4.BeautifulSoup(record, "html.parser")
    for item in soup.find_all('li'):
        ret.append(
            u'{0} 聚聚捐赠了 {1} 元'.format(
                item.find(class_='nickname').get_text(),
                item.find(class_='money').get_text()
            )
        )
    return ret
