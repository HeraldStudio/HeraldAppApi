# -*- coding: utf-8 -*-
import time
import json

from BaseHandlerh import BaseHandler
import Database.tables
from Database.tables import Topic,Likes,Comment
import commonFunctions


class CommentActivity(BaseHandler):  #评论活动
    current_time = time.time()
    def post(self):
        retjson = {'code': '', 'content': ''}
        m_topicId = self.get_argument('topicId', default='unsolved')  # 话题名
        m_user_phone = self.get_argument('phone', default='unsolved')
        m_content = self.get_argument('comment', default='unsolved')
        try:
             exist = self.db.query(Comment).filter(Comment.topicId == m_topicId,
                                                   Comment.user_phone == m_user_phone,
                                                   Comment.content == m_content).one()
             if exist:
                 retjson['code'] = 400
                 retjson['content'] = '该评论已存在'
        except:
                comment = Comment(
                topicId=m_topicId,
                user_phone=m_user_phone,
                content=m_content,
                likeNumber=0,
                time=self.current_time
                )
                self.db.merge(comment)
                retjson['code'] = 200
                retjson['content'] = "评论成功"  # list array
                commonFunctions.commit(self, retjson)

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))



