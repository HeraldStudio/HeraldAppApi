# -*- coding: utf-8 -*-
''' hxc 5-29 20:00 查询所有活动'''
import json

from sqlalchemy import desc
#import timestamp

from mod.databases.tables import Tcomment
from mod.Basehandler import BaseHandler
from TopicFuncs import TopicFuncs


class TopicHandler(BaseHandler):  #  处理客户端一系列请求

    def judge_user(self, cardnum):
        '''
        todo检验该用户是否合法
        :param cardnum: 一卡通号
        :return: 1/0
        ''' 

        return 1

    def post(self):
        ask_code = self.get_argument('askcode', default='unsolved')
        cardnum = self.get_argument('cardnum')
        retjson = {'code': '200', 'content': 'none'}
        retdata = []
        topic_handler = TopicFuncs(self.db)
        # 发布话题（需管理员）
        if ask_code == '101':
            #todo:待判断话题发布者是否有权限
            t_name = self.get_argument('name')
            t_content = self.get_argument('content')
            topic_handler.add_topic(t_name, t_content, retjson)
        # 删除话题（需管理员）
        elif ask_code == '102':
            # todo:待判断是否有删除权限
            topic_id = self.get_argument('tid')
            topic_handler.delete_topic(topic_id, retjson)

        # 评论话题
        elif ask_code == '103':
            content = self.get_argument('content')
            topic_id = self.get_argument('tid')
            quo = self.get_argument('quo', 1)  # 是否为评论引用，1为不是
            ano = self.get_argument('ano')  # 是否匿名，1为匿名
            topic_handler.comment(content, cardnum, topic_id, quo, ano, retjson)

        # 删除评论
        elif ask_code == '104':
            id = self.get_argument('cid')
            topic_handler.delete_comment(id, cardnum, retjson)

        # 给评论点赞
        elif ask_code == '105':
            comment_id = self.get_argument('cid')
            if self.judge_user(cardnum):
                topic_handler.parase(cardnum, comment_id, retjson)
            else:
                retjson['content'] = '该用户不合法'

        # 取消赞
        elif ask_code == '106':
            comment_id = self.get_argument('cid')
            topic_handler.cancel_parase(cardnum, comment_id, retjson)

        # 获得排名前x条评论
        elif ask_code == '107':
            topic_id = self.get_argument('tid') # 通过对应的话题id获取评论列表
            topic_handler.get_list_top(retjson, topic_id)

        # 获得随机的y条评论
        elif ask_code == '108':
            topic_id = self.get_argument('tid') # 通过对应的话题id获取评论列表
            topic_handler.get_list_random(retjson, topic_id)

        # 获得某个评论所有回复
        elif ask_code == '109':
            pass

        # 获得最新x个话题
        elif ask_code == '110':
            topic_id = self.get_argument('tid') # 通过对应的话题id获取评论列表
            topic_handler.get_topics_list(retjson)

        self.write(json.dumps(retjson, indent=2, ensure_ascii=False))

        # elif type == 'askCommentId':   # 一次性获得某个话题的所有评论,按点赞数-+排序
        #     topicId = self.get_argument('topicId')
        #     try:
        #         allComments = self.db.query(Tcomment).filter(Tcomment.topicId == topicId).order_by(
        #             desc(Tcomment.likeNumber))
        #         for item in allComments:
        #             response = dict(
        #                 commentId=item.commentId,
        #                 phone=item.user_phone,
        #                 content=item.content,
        #                 likeNumber=item.likeNumber,
        #                 time=timestamp.timestamp_datetime(item.time)
        #             )
        #             retdata.append(response)
        #     except:
        #         retdata='当前话题无评论'
        #
        #
        # elif type == 'getMyComments':   # 获得自己所有的对话题的评论
        #     user_phone = self.get_argument('userPhone')
        #     allComments = self.db.query(Tcomment).filter(Tcomment.userId == user_phone).all()
        #     for item in allComments:
        #         response = dict(
        #             commentId=item.commentId,
        #             topicId=item.topicId,
        #             content=item.content,
        #             time=timestamp.timestamp_datetime(item.time),
        #             likeNumber=item.likeNumber
        #         )
        #         retdata.append(response)
        # else:
        #     retjson['code'] = 400
        #     retdata="请在type中添加具体ask的内容：如'askAllTopic'"
        # retjson['content'] = retdata
        # self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        #
        #
