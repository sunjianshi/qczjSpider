#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/7 16:54
# @Author   : zequan.shao
# @File     : RequestPage.py
# @Software : PyCharm

import requests
import random
import logging
import settings
from GetProxies import GetProxy


class PageSource:
    def __init__(self, proxy=False, user_agent=False):
        self.proxy = proxy
        self.user_agent = user_agent

    def page_source(self, url, **params):
        """

        :param url: 请求的链接
        :param params: 请求带的参数，如headers、cookies等
        :return: 如果请求成功，则返回一个response对象；否则返回失败的链接
        """
        if not url:
            raise ValueError("The url is None, should set a URL of web.")
        response = self._request_process(url, **params)
        if response.status_code == 200:
            return response
        else:
            return url

    @staticmethod
    def _set_proxies():
        proxies = GetProxy().get_proies()
        if proxies:
            proxy = random.choice(proxies)
            return {'https': 'https://' + proxy, 'http': 'http://' + proxy}
        else:
            logging.warning('The proies is None, that maybe wait a moment!')
            return None

    @staticmethod
    def _set_user_agent():
        if settings.USER_AGENT:
            user_agent = random.choice(settings.USER_AGENT)
            return user_agent
        else:
            logging.warning('The User-Agent is None, that maybe wait a moment!')
            return None

    def _request_process(self, url, **params):
        """

        :param url: 请求的链接
        :param params: 请求带的参数，如headers、cookies等
        :return: 返回一个response对象
        """
        header = params.get('headers', None) or settings.DEFAULT_HEADER
        proxy = self._set_proxies() if self.proxy else None
        if self.user_agent:
            header['User-Agent'] = self._set_user_agent()
        try:
            response = requests.get(url, headers=header, proxies=proxy, timeout=5)
            return response
        except Exception as e:
            logging.warning('%s' % e)
            self._request_process(url, **params)
