# -*- coding=utf-8 -*-
"""
Created on Aug 10, 2016

@author: corvo
"""

from datetime import datetime

from ..Basehandler import BaseHandler
from sqlalchemy.orm.exc import NoResultFound
from mod.databases.tables import Express
from ..return_code_config import generate_ret


class DeleteRecordHandler(BaseHandler):
    """
    删除某条订单记录, 需要订单id
    请牢记, 已经接单的不可以删除
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET,POST')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)
    def post(self):
        retjson = generate_ret('express',200)
        user = self.get_current_user()
        order_id = self.get_argument("id", default=None)
        if not user:
            retjson = generate_ret("express", 302)
        elif not order_id:
            retjson = generate_ret("express",300)
        else:
            try:
                exist_info = self.db.query(Express).filter(Express.phone == user.phone, \
                    Express.id == order_id).one()
                if info.receiving:
                    retjson = generate_ret("express",304)
                else:
                    try:
                        exist_info.delete()
                        self.db.commit()
                    except:
                        self.db.rollback()
            except NoResultFound:
                retjson = generate_ret("express",410)
            except Exception,e:
                retjson = generate_ret("express",500)
        self.write_back(retjson)
