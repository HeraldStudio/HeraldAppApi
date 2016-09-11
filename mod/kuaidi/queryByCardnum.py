# -*- coding=utf-8 -*-
"""
Created on Aug 10, 2016

@author: corvo
"""

from sqlalchemy import desc

from ..Basehandler import BaseHandler
from mod.databases.tables import Express,Users
from ..return_code_config import generate_ret


class QueryByCardnumHandler(BaseHandler):
    def options(self):
        retjson = {'code':200}
        self.write_back(retjson)

    """
    通过一卡通号码查询之前的订单
    """

    def post(self):
        retjson = generate_ret('express',200)
        page = int(self.get_argument('page',default=1))
        ITEM_NUM_EACHPAGE = 10
        start_index = (page-1)*ITEM_NUM_EACHPAGE
        end_index = page*ITEM_NUM_EACHPAGE-1
        _user = self.get_current_user()
        if not _user:
            retjson = generate_ret("express", 302)
        else:
            try:
                user = self.db.query(Users).filter(Users.phone==_user.phone).one()
                info_array = self.db.query(Express).filter(Express.cardnum == user.cardnum)\
                    .order_by(desc(Express.submittime))[start_index:end_index]
                retarray = []
                for info in info_array:
                    item = {
                        'id': info.id,
                        'sms': info.sms,
                        'user': info.user,
                        'phone': info.phone,
                        'dest': info.dest,
                        'arrival': info.arrival,
                        'locate': info.locate,
                        'weight': info.weight,
                        'sub_time': info.submittime.strftime("%Y-%m-%d %H:%M:%S"),
                        'receiving': info.receiving,
                        'finish': info.finish
                    }
                    retarray.append(item)
                retjson['content'] = retarray
            except Exception,e:
                retjson = generate_ret('express',500,str(e))
        self.write_back(retjson)
