# -*- coding: utf-8 -*-
import time
import json

from sqlalchemy.orm.exc import NoResultFound

from BaseHandlerh import BaseHandler
import Database.tables
from Database.tables import Topic,Likes,Comment
from Database.models import connection


class CommentActivity(BaseHandler):  #评论活动
    def post(self):
        tId = self.get_argument('topicId', default='unsolved')  # 话题名
        uId = self.get_argument('userId',default='unsolved')
        cont = self.get_argument('comment',default='unsolved')
        # ISOTIMEFORMAT ='% Y - % m - % d % X'
        # time = time.strftime(ISOTIMEFORMAT, time.localtime( time.time() ) )
        comment = Comment(
            topicId=tId,
            userId=uId,
            content=cont,
            likeNumber=0)
        self.db.merge(comment)
        self.db.commit()
        retdata = "success" # list array
        retjson = {'code': '404', 'content': 'none'}
        retjson['content'] = retdata
        retjson['code'] = 200
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))



