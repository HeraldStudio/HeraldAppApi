# -*- coding: utf-8 -*-
''' hxc 5-29 20:00 查询所有活动'''
import json

from sqlalchemy import desc

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
                    likeNumber=item.likeNumber,
                    commentNumber=item.commentNumber,
                    content=item.content,
                     # startTime=item.startTime, // python 不支持datatime格式，需自己重新封装，见http://www.cnblogs.com/fengmk2/archive/2010/10/23/python-json-encode-datetime.html
                     #   endTime=item.endTime
                    )
                    retdata.append(response)

        elif type == 'askTopicId':  # 测试后认为直接在askAllActivity后存储各个活动较为方面
            name = self.get_argument('topicName', default='unsolved')
            try:
                entry = self.db.query(Topic).filter(Topic.name == name).one()
                topicId = entry.topicId
                retdata.append('topicId', topicId)
            except:
                retdata='no result found'

        elif type == 'askCommentId':   # 一次性获得某个话题的所有评论,按点赞数-+排序
            topicId = self.get_argument('topicId')
            allComments = self.db.query(Comment).filter(Comment.topicId==topicId).order_by(desc(Comment.likeNumber))
            for item in allComments:
                response = dict(
                    commentId=item.commentId,
                    userId=item.userId,
                    content=item.content,
                    likeNumber=item.likeNumber,
                    time=item.time
                )
                retdata.append(response)

        elif type == 'getMyComments':   # 获得自己所有的对话题的评论
            usId = self.get_argument('userId')
            allComments = self.db.query(Comment).filter(Comment.userId == usId).all()
            for item in allComments:
                response = dict(
                    commentId=item.commentId,
                    topicId=item.topicId,
                    content=item.content,
                    time=item.time,
                    likeNumber=item.likeNumber
                )
                retdata.append(response)
        else:
            retjson['code'] = 400
            retdata="请在type中添加具体ask的内容：如'askAllTopic'"
        retjson['content'] = retdata
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))


