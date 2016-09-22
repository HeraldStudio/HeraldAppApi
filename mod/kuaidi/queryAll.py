# -*- coding=utf-8 -*-
"""
Created on Aug 7, 2016

@author: corvo

"""

from datetime import datetime, timedelta

from sqlalchemy import desc

from ..Basehandler import BaseHandler
from mod.databases.tables import Express
from ..return_code_config import generate_ret

delta = 24


class QueryHandler(BaseHandler):   
    """
    管理员查询所有订单
    查询信息, 十小时之内的资料将会被返回,
    """

    def options(self):
        retjson = {'code':200}
        self.write_back(retjson)

    def post(self):
        retjson = generate_ret("express", 200)
        page = int(self.get_argument('page',default=1))
        ITEM_NUM_EACHPAGE = 20
        start_index = (page-1)*ITEM_NUM_EACHPAGE
        end_index = page*ITEM_NUM_EACHPAGE-1
        express_admin = self.get_express_admin()

        if not express_admin:
            retjson = generate_ret("express", 302)
        else:
            try:
                info = self.db.query(Express).filter(Express.submittime > datetime.now() - timedelta(hours=delta)) \
                    .order_by(desc(Express.submittime))[start_index:end_index]
                retarray = []  # 返回数组
                for _info in info:
                    item = {
                        'id': _info.id,
                        'sms': _info.sms,
                        'user': _info.user,
                        'phone': _info.phone,
                        'dest': _info.dest,
                        'arrival': _info.arrival,
                        'locate': _info.locate,
                        'weight': _info.weight,
                        'sub_time': _info.submittime.strftime("%Y-%m-%d %H:%M:%S"),
                        'receiving': _info.receiving,
                        'finish': _info.finish}
                    retarray.append(item)
                retjson['content'] = retarray
            except Exception,e:
                retjson = generate_ret("express", 500, str(e))
        self.write_back(retjson)
        
