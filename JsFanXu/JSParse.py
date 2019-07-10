#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/7 17:39
# @Author   : zequan.shao
# @File     : JSParse.py
# @Software : PyCharm

import settings
import logging
import time
import re
import os
from RequestPage import PageSource
from logging.handlers import TimedRotatingFileHandler
from Re_done import CONTENT

if not os.path.exists('./log'):
    os.makedirs('./log')

logger = logging.getLogger('WrongURL')
logger.setLevel(logging.WARNING)
ch = TimedRotatingFileHandler('./log/UrlLog' + str(time.strftime('%Y-%m-%d')) + '.txt', when='D', encoding='utf-8')
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
ch.setFormatter(formatter)
logger.addHandler(ch)


class JSParse:
    def __init__(self):
        self.proxy = settings.PROXIES_SIGN
        self.user_agent = settings.USER_AGENT_SIGN
        self._var_dict = dict()

    def get_page(self, url, **params):
        """
        获取页面对象
        :param url: 请求的链接
        :param params: 请求所带的参数
        :return: 返回一个页面源代码
        """
        page_object = PageSource(proxy=self.proxy, user_agent=self.user_agent)
        page_source = page_object.page_source(url, **params)
        page = ''
        if isinstance(page_source, str):
            logging.warning('(错误链接)==>%s' % page_source)
        else:
            page = page_source.text
        return page

    @staticmethod
    def get_str_all(page):
        """
        获取所有类似于<script>function Yt_()...(document);</script>的字符串
        :param page: 页面HTML源代码
        :return: 类似于<script>function Yt_()...(document);</script>字符串的列表
        """
        result = re.findall(settings.PARTTEN_STR, page)
        return result

    def get_var(self, str_result):
        """
        :param str_result: 一个类似(function(Yr_))(document);的字符串的列表
        :return: 标签类名和变量值对应的字典。
        """
        result_dict = dict()
        for res in str_result:
            var_dict = dict()
            # 筛选 var Yt_ = ''; 格式
            demo_01 = re.findall(settings.PARTTEN_01, res)
            for ks, vs in demo_01:
                var_dict[ks] = vs

            # 筛选 var Yt_ = function(){...}
            demo_02 = re.findall(settings.PARTTEN_02, res)
            for demo_res_02 in demo_02:
                demo_res_02_res = re.findall("var\s?(\S\S_).*return\s?'(.*?)'", demo_res_02)
                if demo_res_02_res:
                    var_dict[demo_res_02_res[0][0]] = demo_res_02_res[0][1]

            # 筛选 function Yt_(){...}
            demo_03 = re.findall(settings.PARTTEN_03, res)
            var_none_name = []
            for demo_res_03 in demo_03:
                demo_res_03_res = re.findall("function\s?(\S\S_).*return\s?'([a-z]+|[A-Z]+|[0-9;,_]+|[\u4e00-\u9fbb]+|[,]|[;]|[0-9A-Za-z\u4e00-\u9fbb]+)'?;", demo_res_03)
                if demo_res_03_res:
                    var_dict[demo_res_03_res[0][0]] = demo_res_03_res[0][1]
                else:
                    var_none_name.extend(re.findall("function\s?(\S\S_)", demo_res_03))
            # 补充demo_03中因为值在else中而没有被筛选到的情况
            if var_none_name:
                demo_05 = re.findall(settings.PARTTEN_05, res)
                extra_var_dict = dict()
                for demo_res_05 in demo_05:
                    demo_res_05_res = ''.join(re.split('function\s?', demo_res_05)[-2:])
                    if len(demo_res_05_res) < 210:
                        res_05 = re.findall("(\S\S_).*return\s?'([a-z]+|[A-Z]+|[0-9;,_]+|[\u4e00-\u9fbb]+|[,]|[;]|[A-Za-z\u4e00-\u9fbb]+)'?;", demo_res_05_res)
                        if res_05:
                            extra_var_dict[res_05[0][0]] = res_05[0][1]
                if extra_var_dict:
                    for none_name in var_none_name:
                        try:
                            var_dict[none_name] = extra_var_dict[none_name]
                        except KeyError as e:
                            print('-<%s>-变量没有找到对应的属性值!' % none_name)
                            save_var = re.findall("function\s?%s\(\)\s?\{.*?return.*?if.*?return.*?return.*?\}" % none_name, res)
                            print(save_var)
                            # print(res)
                            sec_str = re.findall(
                                "(\S\S_).*return\s?'([a-z]+|[A-Z]+|[0-9;,_]+|[\u4e00-\u9fbb]+|[,]|[;]|[A-Za-z\u4e00-\u9fbb]+)'?;",
                                save_var[0])
                            print(sec_str)
                            if sec_str:
                                var_dict[none_name] = sec_str[0][1]

                            time.sleep(3)

            # 筛选qR_('mp')直接定义的类型
            demo_04 = re.findall(settings.PARTTEN_03, res)
            for demo_res_04 in demo_04:
                demo_res_04_res = re.findall("(\S\S_)\('(.*?)'\)", demo_res_04)
                if demo_res_04_res:
                    var_dict[demo_res_04_res[0][0]] = demo_res_04_res[0][1]

            self._var_dict = var_dict
            dict_r, list_r = self._rule_dict_list(res)
            span_class_name = self._get_class_name(res)

            index = 0
            for coo in list_r.split(';'):
                inde = ''
                for co in coo.split(','):
                    try:
                        inde += dict_r[int(co)]
                    except IndexError as index_e:
                        print(index_e)
                        print(co)
                        # print(res)
                        print(coo)
                        print(len(dict_r))
                        print(dict_r)
                        print(list_r)
                        print('===========================================')
                        inde += ''
                result_dict[span_class_name.replace('$index$', str(index))] = inde
                index += 1
        return result_dict

    @staticmethod
    def _get_class_name(res):
        """
        获取当前res字符串内容的$GetClassName$方法中的需要替换的标签类名
        :param res: 一个类似(function(Yr_))(document);的字符串
        :return: 需要替换的类名格式
        """
        class_first_name = re.findall(settings.PARTTEN_CLASSNAME, res)
        class_done_name = re.sub("[ '\.\+]", '', class_first_name[0])
        return class_done_name

    def _rule_dict_list(self, res):
        """
        获取ruleDict 字体集和rulePosList字体顺序集
        :param res: 一个类似(function(Yr_))(document);的字符串
        :return: dict_r 字体集， list_r 字体顺序集
        """
        # 取ruleDict的内容
        rule_dict = re.findall(settings.PARTTEN_RULEDICT, res)
        split_dict = rule_dict[0].split('+')
        rule_list = re.findall(settings.PARTTEN_RULELIST, res)
        split_list = rule_list[0].split('+')
        try:
            dict_r = ''.join(map(self._map_rule, split_dict))
            list_r = ''.join(map(self._map_list, split_list))
        except KeyError as e:
            print(res)
        return dict_r.replace("'", ''), list_r

    def _map_list(self, x):
        if 'function' in x:
            return ''.join(re.findall("return\s?'(.*?)'", x)) or ''.join(re.findall("'([0-9;,]+)'", x))
        elif re.findall("\S\S_\('[0-9,;]+'\)", x):
            return ''.join(re.findall("\S\S_\('([0-9,;]+?)'\)", x))
        elif re.findall('\S\S_.*', x):
            return self._var_dict[''.join(re.findall('(\S\S_)', x))]
        elif re.findall("'[0-9,;]+'", x):
            return ''.join(re.findall("'([0-9,;]+)'", x))
        else:
            if x == "''":
                return ''
            else:
                return x

    def _map_rule(self, x):
        if 'function' in x:
            return ''.join(re.findall("return\s?'(.*?)'", x)) or ''.join(re.findall("\('([A-Za-z\u4e00-\u9fbb]+)'\)", x))
        elif re.findall("\('[A-Za-z\u4e00-\u9fbb]+'\)", x):
            return ''.join(re.findall("\('([A-Za-z\u4e00-\u9fbb]+)'\)", x))
        elif re.findall('\S\S_.*', x):
            return self._var_dict[''.join(re.findall('(\S\S_)', x))]
        else:
            if x == "''":
                return ''
            else:
                return x


# if __name__ == '__main__':
#     resu = JSParse().get_str_all(CONTENT)
#     print(JSParse().get_var(resu))
