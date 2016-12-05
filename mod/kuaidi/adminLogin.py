# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import hashlib
import json,uuid
from sqlalchemy.orm.exc import NoResultFound
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import ExpressAdmin
from ..return_code_config import generate_ret


class ExpressAdminLoginHandler(BaseHandler):
    def post(self):
        retjson = generate_ret('express', 200)
        admin_name = self.get_argument('admin_name', None)
        pwd = self.get_argument('password', None)
        if not admin_name or not pwd:
            retjson = generate_ret('express', 300)
        else:
            try:
                user = self.db.query(ExpressAdmin).filter(ExpressAdmin.name == admin_name).one()
                if pwd == user.password:
                    token = uuid.uuid1()
                    user.token = str(token)
                    self.db.add(user)
                    self.db.commit()
                    retjson['content'] = str(token)
                else:
                    retjson = generate_ret('express', 400)
            except NoResultFound:
                retjson = generate_ret('express', 301)
            except:
                retjson = generate_ret('express', 500)
        self.write_back(retjson)
