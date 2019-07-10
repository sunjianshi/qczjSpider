#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/16 11:52
# @Author   : zequan.shao
# @File     : JS2Data.py
# @Software : PyCharm

import re
import settings
import json
from Re_done import CONTENT
from JSParse import JSParse


class JS2Data:
    def __init__(self, page, result_dict):
        """
        :param page: 页面源代码
        :param result_dict: 这里面存的是标签类名和值的对应
        """
        self._page = page
        self._result_dict = result_dict

    def get_config(self):
        """
        提取页面字符串
        :return:
        """
        config = re.findall(settings.PARTTEN_CONFIG, self._page)
        config = self._replace(config[0])
        return json.loads(config[:-1], encoding='utf-8')

    def get_option(self):
        """提取option配置信息"""
        option = re.findall(settings.PARTTEN_OPTION, self._page)
        option = self._replace(option[0])
        return json.loads(option[:-1], encoding='utf-8')

    def get_color(self):
        color = re.findall(settings.PARTTEN_COLOR, self._page)
        color = self._replace(color[0])
        return json.loads(color[:-1], encoding='utf-8')

    def get_inner_color(self):
        inner_color = re.findall(settings.PARTTEN_INNERCOLOR, self._page)
        inner_color = self._replace(inner_color[0])
        return json.loads(inner_color[:-1], encoding='utf-8')

    def _replace(self, strs):
        if not isinstance(self._result_dict, dict):
            raise TypeError('The _result_dict must be dict, not %s.' % type(self._result_dict))
        for class_name, values in self._result_dict.items():
            strs = strs.replace("<span class='" + class_name + "'></span>", values)
        return strs

    @staticmethod
    def parse_config_option(cont_dict, sign=''):
        if not isinstance(cont_dict, dict):
            raise TypeError('The type of content must be dict, not %s.' % type(cont_dict))
        if cont_dict.get('message'):  # == '成功'
            car_info = dict()
            if sign == 'config':
                for item in cont_dict.get('result').get('paramtypeitems'):
                    for de_item in item.get('paramitems'):
                        for detail_item in de_item.get('valueitems'):
                            if not isinstance(car_info.get(detail_item.get('specid')), dict):
                                car_info[detail_item.get('specid')] = dict()
                            car_info[detail_item.get('specid')][de_item.get('name')] = detail_item.get('value')
            elif sign == 'option':
                for item in cont_dict.get('result').get('configtypeitems'):
                    for de_item in item.get('configitems'):
                        for detail_item in de_item.get('valueitems'):
                            if not isinstance(car_info.get(detail_item.get('specid')), dict):
                                car_info[detail_item.get('specid')] = dict()
                            car_info[detail_item.get('specid')][de_item.get('name')] = detail_item.get('value')
            else:
                raise ValueError('The sign is not in("option", "config").')
            return car_info
        else:
            print('(parse_config_option)==>Error: message is %s!' % cont_dict.get('message'))

    @staticmethod
    def parse_color(color_dict, sign):
        if not isinstance(color_dict, dict):
            raise TypeError('The type of content must be dict, not %s.' % type(color_dict))
        car_color_info = dict()
        for item in color_dict.get('result').get('specitems'):
            if not isinstance(car_color_info.get(item.get('specid')), dict):
                car_color_info[item.get('specid')] = dict()
            for ite in item.get('coloritems'):
                car_color_info[item.get('specid')][ite.get('name') + str(sign)] = ite.get('value')
        return car_color_info


# if __name__ == '__main__':
#
#     resu = JSParse().get_str_all(CONTENT)
#     # print(JSParse().get_var(resu))
#     pa = JS2Data(CONTENT, JSParse().get_var(resu))
#     # print(pa.get_inner_color())
#     confi = pa.get_config()
#     optio = pa.get_option()
#     color = pa.get_color()
#     inner_color = pa.get_inner_color()
#     # print(confi)
#     done_config = pa.parse_config_option(confi, sign='config')
#     done_option = pa.parse_config_option(optio, sign='option')
#     done_color = pa.parse_color(color, '-外')
#     done_inner_color = pa.parse_color(inner_color, '-内')
#     for k, v in done_config.items():
#         done_config[k].update(done_option[k])
#         done_config[k].update(done_color[k])
#         done_config[k].update(done_inner_color[k])
#         # new_dict = v
#         # new_dict.update(done_option[k])
#         # done_config[k] = new_dict
#
#     for k, v in done_config.items():
#         print(k, v)

