#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/7 16:59
# @Author   : zequan.shao
# @File     : GetProxies.py
# @Software : PyCharm

import settings
import cx_Oracle


class GetProxy:
    def __init__(self):
        pass

    def _proxies_from_sql(self):
        sql = "SELECT IP FROM PROXIES"
        try:
            conn = self._sql_connect()
            cursor = conn.cursor()
        except Exception as e:
            print('数据库连接错误！--》%s' % e)
            return []

        try:
            result = cursor.execute(sql)
            ips = [res[0].strip() for res in result.fetchall()]
        except Exception as e:
            print('%s--Error: %s.' % (__file__, e))
            ips = []
        finally:
            cursor.close()
            conn.close()
        return ips

    @staticmethod
    def _sql_connect():
        conn = cx_Oracle.connect(settings.PRO_USER, settings.PRO_PASSWD, settings.PRO_HOST + '/' + settings.PRO_SID)
        return conn

    def get_proies(self):
        return self._proxies_from_sql()
