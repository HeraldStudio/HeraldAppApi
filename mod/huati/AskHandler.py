# -*- coding: utf-8 -*-
''' hxc 5-29 20:00 查询所有活动'''
import json

from sqlalchemy import desc
import timestamp
from BaseHandlerh import BaseHandler
from Database.tables import Topic,Comment

class AskHandler(BaseHandler):  #  处理客户端一系列请求
    def post(self):
        type = self.get_argument('type', default='unsolved')
        retjson = {'code': '200', 'content': 'none'}
        retdata = []  # list array
        if type == 'askAllTopic':  # 请求所有活动
            data = self.db.query(Topic).all()  # 返回的是元组
            for item in data:
                    response = dict(
                    topicId=item.topicId,    # item后的字串应与数据表中一致。
                    name=item.name,
                    likeNumber=item.like_number,
                    commentNumber=item.comment_number,
                    content=item.content,
                    startTime=item.start_time,
                    endTime=item.end_time
                    )
                    retdata.append(response)


        elif type == 'askCommentId':   # 一次性获得某个话题的所有评论,按点赞数-+排序
            topicId = self.get_argument('topicId')
            try:
                allComments = self.db.query(Comment).filter(Comment.topicId == topicId).order_by(
                    desc(Comment.likeNumber))
                for item in allComments:
                    response = dict(
                        commentId=item.commentId,
                        phone=item.user_phone,
                        content=item.content,
                        likeNumber=item.likeNumber,
                        time=timestamp.timestamp_datetime(item.time)
                    )
                    retdata.append(response)
            except:
                retdata='当前话题无评论'


        elif type == 'getMyComments':   # 获得自己所有的对话题的评论
            user_phone = self.get_argument('userPhone')
            allComments = self.db.query(Comment).filter(Comment.userId == user_phone).all()
            for item in allComments:
                response = dict(
                    commentId=item.commentId,
                    topicId=item.topicId,
                    content=item.content,
                    time=timestamp.timestamp_datetime(item.time),
                    likeNumber=item.likeNumber
                )
                retdata.append(response)
        else:
            retjson['code'] = 400
            retdata="请在type中添加具体ask的内容：如'askAllTopic'"
        retjson['content'] = retdata
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))


