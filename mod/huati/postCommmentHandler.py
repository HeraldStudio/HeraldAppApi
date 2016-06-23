# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2016-03-11 14:02:05
# @Author  : qianxin@live.cn

import hashlib
import json
from sqlalchemy.orm.exc import NoResultFound
from ..Basehandler import BaseHandler
import traceback
from ..databases.tables import Access_Token,Users,Topics,Comments

class PostCommmentHandler(BaseHandler):
    def get(self):
        ret = {'code':200,'content':'ok'}
        self.write(json.dumps(ret,ensure_ascii=False, indent=2))

    def post(self):
        retjson = {'code':200,'content':'ok'}
        topicid =self.get_argument('topic_id',None)
        token = self.get_argument('token',None)
        content =self.get_argument('content',None)
        if not token:
            retjson['code'] = 400
            retjson['content'] = u'用户名密码不能为空'
        else:
            try:
                access_token = self.db.query(Access_Token).filter(Access_Token.phone == phone).one()
                user_phone = access_token.phone
                #activitys = self.db.execute("select * from Act where %s;" % string).fetchall()
                #insert into comments (topicid,content,time,phone) values (topicid,content,time,user_phone)
            	#
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except:
                # print traceback.print_exc()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write_back(retjson)
