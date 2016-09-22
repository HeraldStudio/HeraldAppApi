# -*- coding=utf-8 -*-
"""
Created on Aug 7, 2016

@author: corvo
"""
import json
from datetime import datetime

from ..Basehandler import BaseHandler
from sqlalchemy.orm.exc import NoResultFound
from mod.databases.tables import Express
from mod.databases.tables import ExpressModify
from ..return_code_config import generate_ret


class ModifyStateHandler(BaseHandler):
    """
    工作人员更新快递状态, 通过手机号和订单id确定
    工作人员需要登录
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET,POST')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)
        
    def post(self):
        retjson = generate_ret("express", 200)

        express_admin = self.get_express_admin()
        order_id = self.get_argument("id", default = None)
        state = self.get_argument("state", default = None)
        key = self.get_argument("key", default = None)
        if not (order_id and state and key):
            retjson = generate_ret("express", 300)
        elif not express_admin:
            retjson = generate_ret("express", 302)
        else:
            try:
                if key == "finish" or key == "receiving":
                    state = {'true':True,'false':False}[state]
                    data = { key: state}
                    print order_id, data
                    exist_info = self.db.query(Express).filter(Express.id == order_id).update(data)
                    try:
                        modify = ExpressModify(
                            superuser=express_admin.name,
                            modify=json.dumps(data),
                            modifytime=datetime.now()
                        )
                        self.db.add(modify)
                        self.db.commit()
                    except Exception,e:
                        self.db.rollback()
                        retjson = generate_ret("express", 500, str(e))
                else:
                    retjson = generate_ret("express", 303)
            except NoResultFound:
                retjson = generate_ret("express", 410)
            except Exception,e:
                retjson = generate_ret("express", 500, str(e))
        self.write_back(retjson)
