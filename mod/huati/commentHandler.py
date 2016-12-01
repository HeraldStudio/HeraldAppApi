# -*- coding: utf-8 -*-
import time
import json

from BaseHandlerh import BaseHandler
import Database.tables
from Database.tables import Topic,Likes,Comment
import TopicFuncs


class CommentActivity(BaseHandler):  #评论话题
    current_time = time.time()
    def post(self):
        retjson = {'code': '', 'content': ''}
        m_topicId = self.get_argument('topicId', default='unsolved')  # 话题名
        m_user_phone = self.get_argument('phone', default='unsolved')
        m_content = self.get_argument('comment', default='unsolved')


        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))



