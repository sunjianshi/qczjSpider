#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/20 11:08
# @Author   : zequan.shao
# @File     : MkCarConfigUrl.py
# @Software : PyCharm

import time
import requests
import settings
import random
from lxml import etree
from GetProxies import GetProxy
from queue import Queue



def config_urls(url_list, pool):
    """
    访问初始链接，然后获取当前所有车型的配置信息的链接。
    若访问失败或者代理不可用，都将重新调用此方法。
    :param url: 初始链接
    :return: 车型配置信息链接的列表
    """
    url_items = []
    for url in url_list:
        urls = get_url(url, pool)
        print(urls)
        if urls:
            for url in urls:
                url_items.append(url)
    return url_items

def get_url(url, pool):

    try:

        # proxy_list = GetProxy().get_proies()
        # if proxy_list:
        #     proxy = {
        #         'http': 'http://%s' % random.choice(proxy_list),
        #         'https': 'https://%s' % random.choice(proxy_list),
        #     }
        # else:
        #     proxy = None

        proxy = pool.get()
        response = requests.get(url, headers=settings.DEFAULT_HEADER, proxies=proxy)
        if response.status_code == 200:
            resp = etree.HTML(response.text)
            car_configs = resp.xpath(
                '/html/body/div[@class="content"]/div[@class="row"]/div/div/div[@class="findcont"]/dl/dd/ul/li/div[@class="cont-pic"]/a/@href')
            return list(
                map(lambda x: 'https://car.autohome.com.cn/config/series/%s.html' % x.replace('/', ''), car_configs))
        else:
            print('(%s)==>%s' % (response.status_code, url))
            time.sleep(2)
            get_url(url, pool)
    except Exception as e:
        print('%s(%s)--Error：(%s)==>%s' % (__file__.split('\\')[-1], 'config_urls', e, url))
        time.sleep(2)
        get_url(url, pool)