# coding=utf-8
'''
 @author:黄鑫晨
 @createtime:2016-10-01
 @introduction:话题的一系列函数
'''
import time

from sqlalchemy import func

from mod.databases.tables import Topic, Tpraise, Tcomment, TopicAdmin, Users
from ..databases.db import get_db
global db
db = get_db()

global default_quote_comment_number
default_quote_comment_number = 1
class TopicFuncs(object):

    def commit(self, retjson):
        '''
        提交
        :param db: 数据库引擎
        :param retjson: 要处理的retjson
        :return:null
        '''
        try:
            db.commit()  #  retjson默认为成功情况内容
        except:
            db.rollback()
            retjson['code'] = 408  # Request Timeout
            retjson['content'] = 'Some errors when commit to database, please try again'



    def add_topic(self, t_name, t_content, retjson):
        '''
        添加话题
        :param topic: 话题对象或字典
        :return:success/fail-> 1/0
        '''
        try:
            exist = db.query(Topic).filter(Topic.content == t_content, Topic.name == t_name).one()
            if exist:
                retjson['code'] = 200
                retjson['content'] = "该话题已存在"
        except Exception, e:
            print e
            new_topic = Topic(
             name=t_name,
             content=t_content,
             startT=func.now()  # 开始时间
            )
            db.merge(new_topic)
            self.commit(retjson)
            retjson['code'] = 200
            retjson['content'] = "添加话题成功"


    def delete_topic(self, id, retjson):
        '''
        删除话题
        :param id: 要删除的话题
        :return: success/fail
        '''
        try:
            exist = db.query(Topic).filter(Topic.id == id, Topic.valid == 1).one()
            if exist:
                exist.valid = 0
                self.commit(retjson)
                retjson['code'] = 200
                retjson['content'] = "删除成功"
        except Exception, e:
            print e
            retjson['code'] = 200
            retjson['content'] = "该话题不存在或已删除"

    def delete_comment(self, tid, cardnum, retjson):
        '''
        删除评论
        :param id: 评论Id
        :param cardnum:删除者一卡通号
        :return: 1/0
        '''

        try:
            exist = db.query(Tcomment).filter(Tcomment.id == tid, Tcomment.valid == 1).one()
            if exist:
                # 判断是否为管理员或评论者
                # todo：是否为管理员
                if cardnum == exist.cardnum:
                    exist.valid = 0
                    retjson['content'] = "删除成功"
                    self.commit(retjson)
                else:
                    retjson['content'] = "不是评论者本人或管理员，不能删除"
        except Exception, e:
            print e
            retjson['content'] = "该评论不存在或已删除"

    def comment(self, content, cardnum, tid, quo, ano, retjson):
        '''
        评论话题
        :param content: 评论内容
        :param cardnum: 一卡通号
        :param id: 话题id
        :param quo:是否为评论引用，如果为default_quote_comment_number则不是，否则为评论Id
        :param ano:是否匿名，1为匿名，0为不匿名
        :param retjson: 返回值
        :return: success/fail-> 1/0
        @attention：注意是否是一级评论
        '''
        try:
            u_exist = db.query(Users).filter(Users.cardnum == cardnum).one()
            if u_exist:
                try:
                    exist = db.query(Tcomment).filter(Tcomment.topicid == tid,
                                            Tcomment.cardnum == cardnum,
                                            Tcomment.content == content,
                                            Tcomment.valid == 1).one()
                    if exist:
                        retjson['content'] = '该评论已存在'
                except Exception, e:
                    print e
                    agree = 0  # 是否能评论
                    # 保证只能评论话题或评论一级评论
                    if quo == default_quote_comment_number:  # 为直接评论话题
                        agree = 1
                    else:
                        # 查找出该评论的评论
                        try:
                            comment = db.query(Tcomment).filter(Tcomment.id == quo).one()
                            # 如果该评论评论的是一级评论：
                            if comment.quote == default_quote_comment_number:
                                agree = 1
                        except Exception, e:
                            print e
                            retjson['content'] = '该评论引用有误'
                    # 保证只能评论话题或评论一级评论
                    if agree == 1:
                        new_comment = Tcomment(
                        topicid=tid,
                        cardnum=cardnum,
                        content=content,
                        commentT=func.now(),
                        quote=quo,  # 评论引用，为评论Id，作为一级评论的回复
                        anonymous=ano
                        )
                        db.merge(new_comment)
                        retjson['content'] = '评论成功'
                        self.commit(retjson)


        except Exception, e:
            print e
            retjson['content'] = '该用户不存在'

    def parase(self, cardnum, id):
        '''
        给评论点赞
        :param cardnum: 一卡通号
        :param id:  评论点赞
        :return:
        '''

    def cancel_parase(self, cardnum, id):
        '''
        取消赞
        :param cardnum: 一卡通号
        :param id:赞的Id
        :return: 1/0
        '''
    def get_list_top(self):
        '''
        获得话题前x名的简略信息
        :return: 返回话题前x名的简略列表
        '''

    def get_list_random(self):
        '''
        获得后面随机y个话题
        :return: y个话题的列表
        '''

    def get_list_detail(self):
        '''
        获得话题详细信息列表（预留接口，不一定用）
        :return: 详细信息列表
        '''

    def get_info_simply(self, id):
        '''
        返回话题简略信息
        :param id: 话题id
        :return: 单个话题简略信息
        '''


    def get_info_detail(self, id):
        '''
        返回话题详细信息
        :id:话题id
        :return: 返回单个话题详细信息
        '''


