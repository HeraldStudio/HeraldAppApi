#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
这是供管理员登录的接口，

"""
import random
import hashlib
from mod.Basehandler import ManagerHandler
from mod.cache.cache import cache
from mod.databases.tables import Admin
from sqlalchemy.orm.exc import NoResultFound
import json
import IPython

class AdminLoginHandler(ManagerHandler):
    def get(self):
        self.write('herald webservice!')
    def post(self):
        retjson = {'code': 200, 'content': u'ok'}
        name = self.get_argument('username', None)
        pwd = self.get_argument('password', None)
        if not name or not pwd:
            retjson['code'] = 400
            retjson['content'] = u'用户名密码不能为空'
        else:
            try:
                admin = self.db.query(Admin).filter(Admin.name == name).one()
                password = hashlib.md5(hashlib.md5(pwd).hexdigest().join(admin.salt)).hexdigest()
                if password == admin.pwd:
                    key = str(random.random()+admin.id)
                    self.set_secure_cookie("key", key)
                    cache.update([(key, admin.name)])
                else:
                    retjson['code'] = 400
                    retjson['content'] = u'密码错误'
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except:
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write(json.dumps(retjson,indent=2,ensure_ascii=False))
