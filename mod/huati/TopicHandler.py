# -*- coding: utf-8 -*-
# 增加/删除话题
import json
from sqlalchemy.orm.exc import NoResultFound
from BaseHandlerh import BaseHandler
from Database.tables import Topic, Likes, Comment, CommentLike
import timestamp
import commonFunctions


class AddTopic(BaseHandler):  # 添加话题

    def post(self):
        user_phone = self.get_argument('phone', default='unsolved')  # 用户名
        topic_name = self.get_argument('name', default='unsolved')
        topic_content = self.get_argument('content', default='unsolved')
        m_start_time = self.get_argument('startTime', default='unsolved')
        m_end_time = self.get_argument('endTime', default='unsolved')
        retjson = {'code': '404', 'content': 'none'}
        try:
            exist = self.db.query(Topic).filter(Topic.name == topic_name).one()  # 查看改话题是否存在
            if exist:  # 该话题已存在
                retjson['code'] = '400'
                retjson['content'] = '该话题已存在'

        except NoResultFound:  # 无该话题，可以添加
            new_topic = Topic(
                name=topic_name,
                content=topic_content,
                comment_number=0,
                like_number=0,
                start_time=m_start_time,
                end_time=m_end_time,
                sponsor=user_phone
            )
            retjson['code'] = '200'
            retjson['content'] = '添加话题成功'
            self.db.merge(new_topic)  # 在话题-用户表中加入改项
            commonFunctions.commit(self, retjson)

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))

