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

class ThumbsUpHandler(BaseHandler):
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
                access_token = self.db.query(Access_Token).filter(Access_Token.token == token).one()
                user_phone = access_token.phone
                try:
                    zaninfo = self.db.query(RUsersComments).filter(RUsersComments.phone==user_phone,RUsersComments.commentid==commentid).one()
                    if zaninfo.zan==0:
                    #update ruserscomments (commentsid,phone,zans) values (commentsid,user_phone,1)
                    #update Comments(zans=commentinfo.zans+1) where Comments.commentid==commentid
                    else:
                    #update ruserscomments (commentsid,phone,zans) values (commentsid,user_phone,0)
                    #update Comments(zans=commentinfo.zans-1) where Comments.commentid==commentid
                except NoResultFound:
                    #insert into ruserscomments (commentsid,phone,zans) values (commentsid,user_phone,1)
                    commentinfo=self.db.query(Comments).filter(Comments.commentid==commentid).one()
                    #update Comments(zans=commentinfo.zans+1) where Comments.commentid==commentid
            except NoResultFound:
                retjson['code'] = 301
                retjson['content'] = u'用户不存在'
            except:
                # print traceback.print_exc()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        self.write_back(retjson)
