# -*- coding: utf-8 -*-

import tornado
import json

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound

from BaseHandlerh import BaseHandler
import mod.Database.tables
from mod.database.tables import Topic, Likes,Comment,CommentLike
#from mod.database.models import connection

import TopicFuncs


class LikeActivity(BaseHandler):  # 给话题点赞

    def post(self):
        topicId = self.get_argument('topicId', default='unsolved')  # 话题名
        user_phone = self.get_argument('phone', default='unsolved')  # 用户名
        retjson = {'code': '404', 'content': 'none'}
        retdata = []  # list array
        lnumber = self.db.query(Topic.like_number).filter(Topic.topicId == topicId).scalar()
        try:
            exist = self.db.query(Likes).filter(Likes.topicId == topicId,
                                                Likes.user_phone == user_phone).one()  # 查找话题-用户点赞表，查看用户是否已经就该话题点过赞
            if exist:  # 该用户已对改话题点过赞
                retjson['code'] = '400'
                retjson['content'] = '不能重复点赞'

        except NoResultFound:  # 未点过赞，可以点赞
            lnumber += 1
            like = Likes(
                topicId=topicId,
                user_phone=user_phone)
            self.db.query(Topic).filter(Topic.topicId == topicId).update({"like_number": lnumber})  # 更新
            self.db.merge(like)  # 在话题-用户表中加入改项
            retjson['code'] = 200
            retjson['content'] = "点赞成功"
            TopicFuncs.commit(self, retjson)


        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))


class LikeComment(BaseHandler):  #  给讨论点赞

    def post(self):
        comId = self.get_argument('commentId',default='unsolved')  # 讨论名
        m_user_phone = self.get_argument('phone',default='unsolved')  # 用户名
        result = self.db.query(Comment.like_number).filter(comId == Comment.commentId).one() # comment like number
        clnumber = result.like_number
        retjson = {'code': '404', 'content': 'none'}
        retdata = []  # list array
        try:    # 还需要判断用户是否存在
            exist = self.db.query(CommentLike).filter(CommentLike.commentId == comId, m_user_phone == CommentLike.user_phone).one()  # 查找评论-用户点赞表，查看用户是否已经就该话题点过赞
            if exist:  # 该用户已对改话题点过赞
                retjson['code'] = '400'
                retjson['content'] = '不能重复点赞'

        except NoResultFound:  # 未点过赞，可以点赞
            clnumber += 1
            clike = CommentLike(
                commentId=comId,
                user_phone=m_user_phone)
            self.db.query(Comment).filter(Comment.commentId==comId).update({"like_number": clnumber})  # 更新
            self.db.merge(clike)  # 在话题-用户表中加入改项
            try:
                self.db.commit()  # 修改后一定要commit更新数据库
                response = dict(
                likeNumber=self.db.query(Comment.like_number).filter(Comment.commentId==comId).scalar(),
                reply='点赞成功')
                retdata.append(response)
                retjson['code'] = 200
                retjson['content'] = response
            except Exception, e:
                self.db.rollback()
                retjson['code'] = 400
                retjson['content'] = "store data wrong!Try again"


        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
