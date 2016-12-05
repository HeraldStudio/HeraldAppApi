# -*- coding: utf-8 -*-

'''
 @author:黄鑫晨
 @createtime:2016-10-01
 @introduction:话题的一系列函数
'''
import time
import random

from sqlalchemy import func, desc

from mod.databases.tables import Topic, Tpraise, Tcomment, TopicAdmin, Users

#global db,
from mod.huati.getUserInfo import User_info_handler
global top, random_list_number, default_quote_comment_number, topic_number
top = 10
# top:返回前top的人数
random_list_number = 10
# 默认评论引用
default_quote_comment_number = 1
# 默认返回话题数
topic_number = 10


class TopicFuncs(object):

    def __init__(self, db):
        self.db = db


    def commit(self, retjson):
        '''
        提交
        :param db: 数据库引擎
        :param retjson: 要处理的retjson
        :return:null
        '''
        try:
            self.db.commit()  # retjson默认为成功情况内容
        except Exception, e:
            print (e)
            self.db.rollback()
            retjson['code'] = 408  # Request Timeout
            retjson['content'] = 'Some errors when commit to database, please try again'

    def __is_parased(self, cardnum, each):
        is_parased = 0
        try:
            praise_entry = self.db.query(Tpraise).filter(Tpraise.cardnum == cardnum, Tpraise.commentid == each.id).one()
            # 点过赞
            if praise_entry:
                is_parased = 1
        except Exception, e:
            is_parased = 0
        return is_parased

    def add_topic(self, t_name, t_content, retjson):
        '''
        添加话题
        :param topic: 话题对象或字典
        :return:success/fail-> 1/0
        '''
        try:
            exist = self.db.query(Topic).filter(Topic.content == t_content, Topic.name == t_name).one()
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
            self.db.merge(new_topic)
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
            exist = self.db.query(Topic).filter(Topic.id == id, Topic.valid == 1).one()
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
       # 删除评论
        :param id: 评论Id
        :param cardnum:删除者一卡通号
        :return: 1/0
        '''

        try:
            exist = self.db.query(Tcomment).filter(Tcomment.id == tid, Tcomment.valid == 1).one()
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

    def comment(self, content, cardnum, tid, quo, ano, uuid, retjson):
        '''
        评论话题
        :param content: 评论内容
        :param cardnum: 一卡通号
        :param id: 话题id
        :param quo:是否为评论引用，如果为default_quote_comment_number则不是，否则为评论Id
        :param ano:是否匿名，1为匿名，0为不匿名
        :param uuid:用户的uuid，用来完善真实信息
        :param retjson: 返回值
        :return: success/fail-> 1/0
        @attention：注意是否是一级评论
        '''

        try:
            # TODO 将注释删除
            #u_exist = self.db.query(Users).filter(Users.cardnum == cardnum).one()
            u_exist = True
            if u_exist:
                try:
                    exist = self.db.query(Tcomment).filter(Tcomment.topicid == tid,
                                                      Tcomment.cardnum == cardnum,
                                                      Tcomment.content == content,
                                                      Tcomment.valid == 1,
                                                      Tcomment.quote == quo).one()
                    if exist:
                        retjson['content'] = '该评论已存在'
                # 评论不存在
                except Exception, e:
                    print e
                    try:
                        # 寻找到该话题
                        topic = self.db.query(Topic).filter(Topic.id == tid).one()
                        is_anonymous = False
                        if ano == u'1':         # 此处传来的数据为unicode, 不能直接与数字1比较
                            is_anonymous = True

                        agree = 0  # 是否能评论
                        # 保证只能评论话题或评论一级评论
                        if int(quo) == default_quote_comment_number:  # 为直接评论话题
                             agree = 1
                            # 评论数+1
                             topic.commentN += 1
                        else:
                            print ("error")
                            # 查找出该评论的评论
                            try:
                                comment = self.db.query(Tcomment).filter(Tcomment.id == quo).one()
                                # 如果该评论评论的是一级评论：
                                if comment.quote == default_quote_comment_number:
                                  agree = 1
                            except Exception, e:
                                 print e
                                 retjson['content'] = '该评论引用有误,只能评论一级评论'
                        # 保证只能评论话题或评论一级评论
                        # 完善学生真实姓名
                        user_info_handler = User_info_handler(self.db)
                        user_info_handler.complete_user_name(uuid)
                        if agree == 1:
                            new_comment = Tcomment(
                            topicid=tid,
                            cardnum=cardnum,
                            content=content,
                            commentT=func.now(),
                            quote=quo,  # 评论引用，为评论Id，作为一级评论的回复
                            anonymous=is_anonymous
                            )
                            self.db.merge(new_comment)
                            retjson['content'] = '评论成功'
                            self.commit(retjson)

                    except Exception, e:
                        print e
                        retjson['code'] = '400'
                        retjson['content'] = '该话题不存在'
        except Exception, e:
            print "创建新用户"
            # new_user = Users(
            #     cardnum=cardnum
            # )


    def parase(self, cardnum, cid, retjson):
        '''
        给评论点赞
        :param cardnum: 一卡通号
        :param cid:  评论Id
        :return:
        '''
        try:
            exist = self.db.query(Tpraise).filter(Tpraise.cardnum == cardnum, Tpraise.valid == 1,
                                             Tpraise.commentid == cid).one()
            if exist:
                retjson['content'] = '失败，之前已点过赞'
                retjson['code'] = 300
        except Exception, e:
            print e
            # 查看该评论是否存在：
            try:
                c_exist = self.db.query(Tcomment).filter(Tcomment.id == cid).one()
                c_exist.likeN += 1
                new_parase = Tpraise(
                    cardnum=cardnum,
                    commentid=cid,
                    paraseT=func.now()
                )
                self.db.merge(new_parase)
                retjson['content'] = '点赞成功'
                self.commit(retjson)
            except Exception, e:
                print e
                retjson['content'] = '该评论不存在或已删除'

    def cancel_parase(self, cardnum, cid, retjson):
        '''
        取消赞
        :param cardnum: 一卡通号
        :param id:评论的Id
        :return: 1/0
        '''
        try:
            exist = self.db.query(Tpraise).filter(Tpraise.cardnum == cardnum, Tpraise.valid == 1,
                                             Tpraise.commentid == cid).one()
            if exist:
                exist.valid = 0
                try:
                    c_exist = self.db.query(Tcomment).filter(Tcomment.id == cid).one()
                    c_exist.likeN -= 1
                    retjson['content'] = '取消赞成功'
                    self.commit(retjson)
                except Exception, e:
                    print e
                    retjson['content'] = '该评论以删除或不存在'

        except Exception, e:
            print e
            retjson['content'] = '无点赞记录'

    def get_list_top(self, retjson, tid, cardnum):
        '''
        获得话题前x名评论的简略信息
        :return: 返回话题评论前x名的简略列表
        '''
        default_quote_comment_number = 3
        try:
            tops = self.db.query(Tcomment).order_by(desc(Tcomment.likeN)). \
                filter(Tcomment.id != default_quote_comment_number and Tcomment.topicid == tid).limit(top).all()

            retdata = []
            for each in tops:
                # 该用户是否已经给该评论点过赞，0为没点，1为点过
                is_parased = self.__is_parased(cardnum, each)
                user_info_handler = User_info_handler(self.db)
                comment = user_info_handler.get_comment_model(each, is_parased, each.anonymous)
                retdata.append(comment)
            retjson['content'] = retdata
        except Exception, e:
            print e
            retjson['content'] = '查询出错'

    def get_list_latest(self, retjson, topic_id, cardnum):
        '''
        获得话题最新x名评论的简略信息
        :return: 返回话题最新x名的简略列表
        '''
        user_info_handler = User_info_handler(self.db)

        default_quote_comment_number = 3
        try:
            tops = self.db.query(Tcomment).order_by(desc(Tcomment.commentT)). \
                filter(Tcomment.id != default_quote_comment_number and Tcomment.topicid == topic_id).limit(top).all()

            retdata = []
            for each in tops:
                # 该用户是否已经给该评论点过赞，0为没点，1为点过
                is_parased = self.__is_parased(cardnum, each)
                user_info_handler = User_info_handler(self.db)
                comment = user_info_handler.get_comment_model(each, is_parased, each.anonymous)
                retdata.append(comment)
            retjson['content'] = retdata
        except Exception, e:
            print e
            retjson['content'] = '查询出错'

    def get_list_random(self, retjson, tid, cardnum):
        '''
        获得后面随机y个话题的评论
        :return: y个话题的列表
        '''
        try:
            # 最高的多少名
            # l = [1,2,3,43,4,5,6]
            # random.shuffle(l)
            # retjson['code'] = 'dsds'
            # retjson['content'] = l
            # retjson['code'] = l[-1]
            tops = self.db.query(Tcomment).order_by(desc(Tcomment.likeN)). \
                 filter(Tcomment.id != default_quote_comment_number and Tcomment.topicid == tid).limit(top).all()

            last = tops[-1]
            least_likeN = last.likeN
            comments = self.db.query(Tcomment).filter(Tcomment.id != default_quote_comment_number,
                                                 Tcomment.likeN<least_likeN).all()
            # 打乱
            random.shuffle(comments)
            retdata = []
            for each in comments[0:random_list_number]:
                # 匿名
                if each.anonymous:
                    comment = dict(
                        time=each.commentT.strftime('%Y-%m-%d %H:%M:%S'),
                        cardnum='匿名小公举'.decode('utf-8'),
                        likeN=each.likeN,
                        content=each.content
                    )
                    print(comment)
                else:
                    comment = dict(
                        time=each.commentT.strftime('%Y-%m-%d %H:%M:%S'),
                        cardnum=each.cardnum,
                        likeN=each.likeN,
                        content=each.content
                    )
                    retdata.append(comment)
            retjson['content'] = retdata
        except Exception, e:
            print e

    def get_topics_list(self, retjson):
        '''
        返回最新x个话题简略信息列表
        :return:列表
        '''
        try:
            topics = self.db.query(Topic).filter(Topic.valid == 1).order_by(desc(Topic.startT)).limit(topic_number).all()
            retdata = []
            for topic in topics:
                retdata.append(self.get_info_simply(topic.id))

        except Exception, e:
            print e
        retjson['content'] = retdata

    def get_list_detail(self):
        '''
        获得话题详细信息列表（预留接口，不一定用）
        :return: 详细信息列表
        '''
        pass

    def get_info_simply(self, id):
        '''
        返回话题简略信息
        :param id: 话题id
        :return: 单个话题简略信息
        '''
        try:
            topic = self.db.query(Topic).filter(Topic.id == id, Topic.valid == 1).one()
            ret_topic = dict(
                id=topic.id,
                name=topic.name,
                startT=topic.startT.strftime('%Y-%m-%d %H:%M:%S'),
                content=topic.content,
                commentN=topic.commentN
            )
            return ret_topic
        except Exception, e:
            return "该话题不存在或已失效"

    def get_info_detail(self, id):
        '''
        返回话题详细信息
        :id:话题id
        :return: 返回单个话题详细信息
        '''
        pass

    def get_comment_reply(self, cid, retjson):
        '''
        获得某个评论全部回复
        :param cid:评论Id
        :param retjson:返回json
        :return:
         '''
        pass

