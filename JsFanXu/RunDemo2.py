#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/11/20 10:39
# @Author   : zequan.shao
# @File     : RunDemo.py
# @Software : PyCharm

import settings
from IPython import embed
import cx_Oracle
import os
import requests
from lxml import etree
from JSParse import JSParse
from JS2Data import JS2Data
from MkCarConfigUrl import config_urls
from IPPool import IPPoolManager
from getUrl import get_url


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# def name_map():
#     conn = cx_Oracle.connect(settings.MID_USER, settings.MID_PASSWD, settings.MID_HOST + '/' + settings.MID_SID)
#     cursor = conn.cursor()
#     sql = "SELECT CHINA_NAME,DBBASE_NAME FROM KOUBEI_DB_NAME"
#     search_result = cursor.execute(sql)
#     res = search_result.fetchone()
#     names_dict = dict()
#     while res:
#         names_dict[res[0]] = res[1]
#         res = search_result.fetchone()
#     cursor.close()
#     conn.close()
#     return names_dict


def storage(cont_dict, cx):
    # names_dict = name_map()
    print('cont_dict:',cont_dict)
    new_list = []
    # names_dict = {'d':1}
    # new_dict = settings.item()
    # new_dict = dict()
    # new_dict['SUOSHUCX'] = cx
    # for spk, spv in names_dict.items():
    #     new_dict[spv] = ''
    for bk, bv in cont_dict.items():
        new_dict = settings.item()
        new_dict['SUOSHUCX'] = cx
        # print('bv:',bv)
        for k, v in new_dict.items():
            if v in bv.keys():
                new_dict[k] = bv[v]
            else:
                new_dict[k] = ''
        new_dict['ID'] = str(bk)
        index = 1

        for sk, sv in bv.items():
            if '-外' in sk:
                if index > 10:
                    continue
                new_dict['COLOR%s' % str(index)] = sk + sv
                index += 1
            elif '-内' in sk:
                if index > 10:
                    continue
                new_dict['COLOR%s' % str(index)] = sk + sv
                index += 1

        # embed()
        print(new_dict)
                # try:
                # new_dict[sk] = sv
                # except KeyError as e:
                #     print(sk)
        new_list.append(new_dict)
        conn = cx_Oracle.connect(settings.STO_USER, settings.STO_PASSWD, settings.STO_HOST + '/' + settings.STO_SID)
        cursor = conn.cursor()
        # # try:
        # sql = "INSERT INTO CRAW_CAR_CONFIG VALUES(:ID,:CARNAME,:CSZDJ,:CS,:JIBIE,:NYLX,:SHANGSSJ,:ZUIDAGL,:ZUIDANJ,:FDJ,:BIANSX,:CHANGKG,:CHESJG,:ZUIGCS,:GUANGF0_100JS,:SHIC0_100JS,:SHIC0_100ZD,:GONGXBZHYH,:SHICYH,:ZHENGCZB,:CHANGDU,:KUANDU,:GAODU,:ZHOUJU,:QIANLUNJU,:HOULUNJU,:ZUIXLDJX,:CHEMENSHU,:ZUOWEISHU,:YOUXRJ,:XINGLXRJ,:ZHENGBZL,:FADJXH,:PAILIANGML,:PAILIANGL,:JINQXS,:QIGPLXS,:QIGANGSHU,:MEIGQMS,:YANSUOBI,:PEIQJG,:GANGJIN,:XINGCHENG,:ZUIDAML,:ZUIDAGLZS,:ZUIDANJZS,:FADJTYJS,:RANLIAOXS,:RANYOUBH,:GONGYOUFS,:GANGGCL,:GANGTCL,:HUANBBZ,:DANGWEIGS,:BIANSUXIANGLX,:JIANCHENG,:QUDONGFS,:SIQUXINGS,:ZHONGYCSQJG,:QIANXJLX,:HOUXJLX,:ZHULILX,:CHETIJG,:QIANZDQLX,:HOUZDQLX,:ZHUCZDLX,:QIANLTGG,:HOULTGG,:BEITGG,:ZHUFUJSZAQQL,:QIANHOUPCQL,:QIANHOUPTBQL,:XIBUQL,:TAIYAJCZZ,:LINGTYJXXS,:ANQDWXTS,:ISOFINERTZYJK,:ABSFANGBS,:ZHIDLFP,:SHACFZ,:QIANYINLKZ,:CHESHENWDKZ,:BINGXFZ,:CHEDPLYJXT,:ZHUDSCZDAQXT,:YESHIXT,:PILJSTS,:QIANHZCLD,:DAOCESPYX,:QUANJSXT,:DINGSXH,:ZISYXH,:ZIDBCRW,:FADJQTJS,:SHANGPFZ,:ZIDONGZC,:DOUPOHJ,:KEBXJ,:KONGQXJ,:DIANCGYXJ,:KEBZXB,:QIANQXHCSQ,:ZHONGYCSQSZGN,:HOUQXHCSQ,:ZHENGTZDZXXT,:DIANDTC,:QUANJTC,:YUNDWGTJ,:LVHJLQ,:DIANDXHM,:CEHUAM,:DIANDHBX,:GANYHBX,:CHEDXLJ,:FADJDZFD,:CHENZKS,:YAOKYS,:WUYSQDXT,:WUYSJRXT,:YUANCQD,:PIZFXP,:FANGXPTJ,:FANGXPDDTJ,:DUOGNFXP,:FANGXPHD,:FANGXPJR,:FANGXPJY,:XINGCDNXSP,:QUANYJBP,:HUDTAITSZXS,:NEIZXCJLY,:ZHUDJZ,:SHOUJWXCD,:ZUOYCZ,:YUNDFGZY,:ZUOYGDTJ,:YAOBZCTJ,:JIANBZCTJ,:ZHUFJSZDDTJ,:DIEPKBJDTJ,:DIEPZYYD,:HOUPZYDDTJ,:FUJSWHPKTJAN,:DIANDZYJY,:QIANHPZYJR,:QIANHPZYTF,:QIANHPZYAM,:DIEPDLZY,:DISPZY,:HOUPZYFDFS,:QIANHZYFS,:HOUPHJ,:KEJRZLHJ,:GPSDAOHXT,:DAOLJYHJ,:ZHONGKTCSDP,:ZHONGKTCSDPCC,:ZHONGKYJPFPXS,:LANYCZDH,:SHOUJHLYS,:CHELW,:CHEZDS,:HOUPYJP,:DIANYUAN,:WAIJYYJK,:CDDVD,:YANGSQPP,:YANGSQSL,:JINGD,:YUANGD,:LEDRIJXCD,:ZISYYJG,:ZIZTD,:ZHUANGXFZD,:ZHUANXTD,:QIANWD,:DADGDKT,:DADQXZZ,:CHENFWD,:QIANHDDCC,:CHECYJSJ,:CHECFJSGN,:FANGZWXGRBL,:HOUSJDDTJ,:HOUSJJR,:NEIWHSJZDFXM,:LIUMTCNHSJ,:HOUSJDDZD,:HOUSJJY,:HOUFDZYL,:HOUPCZYL,:HOUPCYSBL,:ZHEYBHZJ,:HOUYS,:GANYYS,:KONGTKZFS,:HOUPDLKT,:HOUZCFK,:WENDFQKZ,:CHENKQTJ,:CHEZKQJHQ,:CHEZBX,:COLOR1,:COLOR2,:COLOR3,:COLOR4,:COLOR5,:COLOR6,:COLOR7,:COLOR8,:COLOR9,:COLOR10,:DUOTC,:SHOUJHLYSGN,:SUOSHUCX,:GONGXBCDXSLC,:KUAICDLBFB,:CHEXJY,:CHEXINGHJ,:HOUPAQDSQL,:SHICEXHLC,:KUAICSJ,:MANCSJ,:SHICEKCSJ,:SHICEMCSJ,:DIANJLX,:CHEDBCFZXT,:DADYSGB,:CHUMSYDD,:FANGZWXBL,:WAIHSJGN,:NEIHSJGN,:KEJIARPSZ,:CHENPMGLZB,:FULZFSQ,:CHENXFZZ,:XINGLXVDYJK,:USBJKSL,:HOUPKZDMT,:SHOUSKZ,:YUYSBKZXT,:DAOHLKXXXS,:ZHONGKYJPCC,:ZHONGKCSYJPM,:HOUPZYDDFD,:HOUPZYFDXS,:HOUPXZB,:DIEPZYTJ,:FUZYTJFS,:ZHUZYTJFS,:DIANDKDTB,:FANGXPCZ,:ZHUDBHSJQGS,:YAOSLX,:WEIMBLDLKQ,:DIANDHBXWZJY,:LUNQCZ,:TIANCLX,:SHESGYXT,:ZIDJSJS,:XUNHXT,:DAOCCCYJXT,:JIASFZYX,:DAOLJTBSSB,:TAIYJCGN,:BEIDXRBH,:HOUPAQSQL,:QIANPZYGN,:GANYYSGN,:JIASMSQH,:CHECYJSJGN,:YEJYBCC,:DIANDJZGL,:DIANDJZNJ,:QIANDDJZDGL,:QIANDDJZDNJ,:HOUDDJZDGL,:HOUDDJZDNJ,:XITZHGL,:XITZHNJ,:QUDDJS,:DIANJBJ,:DIANCLX,:GONGXBXHLC,:DIANCRL,:BAIGLHDL,:DIANCZZB,:KUAICDL,:DIANDJ,:CHENHJFWD,:ZUOYBJ,:HOUPZYGN,:YANGSQPPMC,:DUOCGYBL,:CHECJTB,:QIANDDYWMS,:DENGGTEGN,:XIANHCSQ)"
        sql = "INSERT INTO CRAW_CAR_CONFIG_BF1 VALUES(:ID,:CARNAME,:CSZDJ,:CS,:JIBIE,:NYLX,:SHANGSSJ,:ZUIDAGL,:ZUIDANJ,:FDJ,:BIANSX,:CHANGKG,:CHESJG,:ZUIGCS,:GUANGF0_100JS,:SHIC0_100JS,:SHIC0_100ZD,:GONGXBZHYH,:SHICYH,:ZHENGCZB,:CHANGDU,:KUANDU,:GAODU,:ZHOUJU,:QIANLUNJU,:HOULUNJU,:ZUIXLDJX,:CHEMENSHU,:ZUOWEISHU,:YOUXRJ,:XINGLXRJ,:ZHENGBZL,:FADJXH,:PAILIANGML,:PAILIANGL,:JINQXS,:QIGPLXS,:QIGANGSHU,:MEIGQMS,:YANSUOBI,:PEIQJG,:GANGJIN,:XINGCHENG,:ZUIDAML,:ZUIDAGLZS,:ZUIDANJZS,:FADJTYJS,:RANLIAOXS,:RANYOUBH,:GONGYOUFS,:GANGGCL,:GANGTCL,:HUANBBZ,:DANGWEIGS,:BIANSUXIANGLX,:JIANCHENG,:QUDONGFS,:SIQUXINGS,:ZHONGYCSQJG,:QIANXJLX,:HOUXJLX,:ZHULILX,:CHETIJG,:QIANZDQLX,:HOUZDQLX,:ZHUCZDLX,:QIANLTGG,:HOULTGG,:BEITGG,:ZHUFUJSZAQQL,:QIANHOUPCQL,:QIANHOUPTBQL,:XIBUQL,:TAIYAJCZZ,:LINGTYJXXS,:ANQDWXTS,:ISOFINERTZYJK,:ABSFANGBS,:ZHIDLFP,:SHACFZ,:QIANYINLKZ,:CHESHENWDKZ,:BINGXFZ,:CHEDPLYJXT,:ZHUDSCZDAQXT,:YESHIXT,:PILJSTS,:QIANHZCLD,:DAOCESPYX,:QUANJSXT,:DINGSXH,:ZISYXH,:ZIDBCRW,:FADJQTJS,:SHANGPFZ,:ZIDONGZC,:DOUPOHJ,:KEBXJ,:KONGQXJ,:DIANCGYXJ,:KEBZXB,:QIANQXHCSQ,:ZHONGYCSQSZGN,:HOUQXHCSQ,:ZHENGTZDZXXT,:DIANDTC,:QUANJTC,:YUNDWGTJ,:LVHJLQ,:DIANDXHM,:CEHUAM,:DIANDHBX,:GANYHBX,:CHEDXLJ,:FADJDZFD,:CHENZKS,:YAOKYS,:WUYSQDXT,:WUYSJRXT,:YUANCQD,:PIZFXP,:FANGXPTJ,:FANGXPDDTJ,:DUOGNFXP,:FANGXPHD,:FANGXPJR,:FANGXPJY,:XINGCDNXSP,:QUANYJBP,:HUDTAITSZXS,:NEIZXCJLY,:ZHUDJZ,:SHOUJWXCD,:ZUOYCZ,:YUNDFGZY,:ZUOYGDTJ,:YAOBZCTJ,:JIANBZCTJ,:ZHUFJSZDDTJ,:DIEPKBJDTJ,:DIEPZYYD,:HOUPZYDDTJ,:FUJSWHPKTJAN,:DIANDZYJY,:QIANHPZYJR,:QIANHPZYTF,:QIANHPZYAM,:DIEPDLZY,:DISPZY,:HOUPZYFDFS,:QIANHZYFS,:HOUPHJ,:KEJRZLHJ,:GPSDAOHXT,:DAOLJYHJ,:ZHONGKTCSDP,:ZHONGKTCSDPCC,:ZHONGKYJPFPXS,:LANYCZDH,:SHOUJHLYS,:CHELW,:CHEZDS,:HOUPYJP,:DIANYUAN,:WAIJYYJK,:CDDVD,:YANGSQPP,:YANGSQSL,:JINGD,:YUANGD,:LEDRIJXCD,:ZISYYJG,:ZIZTD,:ZHUANGXFZD,:ZHUANXTD,:QIANWD,:DADGDKT,:DADQXZZ,:CHENFWD,:QIANHDDCC,:CHECYJSJ,:CHECFJSGN,:FANGZWXGRBL,:HOUSJDDTJ,:HOUSJJR,:NEIWHSJZDFXM,:LIUMTCNHSJ,:HOUSJDDZD,:HOUSJJY,:HOUFDZYL,:HOUPCZYL,:HOUPCYSBL,:ZHEYBHZJ,:HOUYS,:GANYYS,:KONGTKZFS,:HOUPDLKT,:HOUZCFK,:WENDFQKZ,:CHENKQTJ,:CHEZKQJHQ,:CHEZBX,:COLOR1,:COLOR2,:COLOR3,:COLOR4,:COLOR5,:COLOR6,:COLOR7,:COLOR8,:COLOR9,:COLOR10,:DUOTC,:SHOUJHLYSGN,:SUOSHUCX,:GONGXBCDXSLC,:KUAICDLBFB,:CHEXJY,:CHEXINGHJ,:HOUPAQDSQL,:SHICEXHLC,:KUAICSJ,:MANCSJ,:SHICEKCSJ,:SHICEMCSJ,:DIANJLX,:CHEDBCFZXT,:DADYSGB,:CHUMSYDD,:FANGZWXBL,:WAIHSJGN,:NEIHSJGN,:KEJIARPSZ,:CHENPMGLZB,:FULZFSQ,:CHENXFZZ,:XINGLXVDYJK,:USBJKSL,:HOUPKZDMT,:SHOUSKZ,:YUYSBKZXT,:DAOHLKXXXS,:ZHONGKYJPCC,:ZHONGKCSYJPM,:HOUPZYDDFD,:HOUPZYFDXS,:HOUPXZB,:DIEPZYTJ,:FUZYTJFS,:ZHUZYTJFS,:DIANDKDTB,:FANGXPCZ,:ZHUDBHSJQGS,:YAOSLX,:WEIMBLDLKQ,:DIANDHBXWZJY,:LUNQCZ,:TIANCLX,:SHESGYXT,:ZIDJSJS,:XUNHXT,:DAOCCCYJXT,:JIASFZYX,:DAOLJTBSSB,:TAIYJCGN,:BEIDXRBH,:HOUPAQSQL,:QIANPZYGN,:GANYYSGN,:JIASMSQH,:CHECYJSJGN,:YEJYBCC,:DIANDJZGL,:DIANDJZNJ,:QIANDDJZDGL,:QIANDDJZDNJ,:HOUDDJZDGL,:HOUDDJZDNJ,:XITZHGL,:XITZHNJ,:QUDDJS,:DIANJBJ,:DIANCLX,:GONGXBXHLC,:DIANCRL,:BAIGLHDL,:DIANCZZB,:KUAICDL,:DIANDJ,:CHENHJFWD,:ZUOYBJ,:HOUPZYGN,:YANGSQPPMC,:DUOCGYBL,:CHECJTB,:QIANDDYWMS,:DENGGTEGN,:XIANHCSQ,:HUOXCC,:ZUIDZZZL,:DIANCCDSJ,:HOUPCMKQFS)"
        # sql = "INSERT INTO CRAW_CAR_CONFIG VALUES(:ID,:CARNAME,:CSZDJ,:CS,:JIBIE,:NYLX,:SHANGSSJ,:ZUIDAGL,:ZUIDANJ,:FDJ,:BIANSX,:CHANGKG,:CHESJG)"
        cursor.execute(sql, new_dict)
        conn.commit()
    # except Exception as e:
        # 测试临时加上的
        # print(e)
        # print(sql)
        # print(new_dict)
    # finally:
        print('存入一条记录！')
        cursor.close()
        conn.close()


if __name__ == '__main__':
    page_parse = JSParse()
    urls = set()  # 用于存储中间访问出现的url
    ippo = IPPoolManager()
    pool = ippo.get_ippool()
    # config_url = config_urls(settings.START_URL_LIST, pool)
    # print(config_url)
    # print(len(config_url))
    # config_url = settings.PZ_URL_LIST
    config_url = get_url()
    if isinstance(config_url, list):
        for ur in config_url:
            urls.add(ur)
        print('(%s)==>%s' % (str(len(urls)), '条链接已经获取！'))
    else:
        print('访问页面出错！')
    # print(urls)
    for per_car in urls:
        # 获取页面js代码，并解析js代码获取类名-变量值字典
        response = requests.get(per_car, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        })
        if response.status_code == 200:
            resp = etree.HTML(response.text)
            cx_title = resp.xpath(
                '/html/body/div[@class="mainWrap sub_nav"]/div[@class="subnav"]/div[@class="subnav-title"]/div[@class="subnav-title-name"]/a/text()')
            print(cx_title)
        else:
            print('(%s)==>访问出错！' % per_car)
            urls.add(per_car)
            continue
        # 得到response 对象
        page = page_parse.get_page(per_car)
        print('per_car:',per_car)
        if not page:
            print('(%s)==>访问出错！' % per_car)
            urls.add(per_car)
            continue
        str_result = page_parse.get_str_all(page)
        print('str_result长度',len(str_result))
        if str_result:
            vars_dict = page_parse.get_var(str_result)
            # 利用解析出来的类名-变量值字典来替换出被加密过后的配置信息
            js2_data = JS2Data(page=page, result_dict=vars_dict)
            config = js2_data.get_config()
            option = js2_data.get_option()
            color = js2_data.get_color()
            inner_color = js2_data.get_inner_color()
            done_config = js2_data.parse_config_option(config, sign='config')
            done_option = js2_data.parse_config_option(option, sign='option')
            done_color = js2_data.parse_color(color, '-外')
            done_inner_color = js2_data.parse_color(inner_color, '-内')
            for k, v in done_config.items():
                done_config[k].update(done_option.get(k, {}))
                done_config[k].update(done_color.get(k, {}))
                done_config[k].update(done_inner_color.get(k, {}))
            # 存储信息
            storage(done_config, cx_title[0])
