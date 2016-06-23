# -*- coding: utf-8 -*-

import tornado
import json

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound

from BaseHandlerh import BaseHandler
import Database.tables
from Database.tables import Topic, Likes,Comment,CommentLike
from Database.models import connection


class LikeActivity(BaseHandler):  # 给话题点赞

    def post(self):
        topicId = self.get_argument('topicId', default='unsolved')  # 话题名
        userId = self.get_argument('userId', default='unsolved')  # 用户名
        retjson = {'code': '404', 'content': 'none'}
        retdata = []  # list array
        lnumber = self.db.query(Topic.likeNumber).filter(Topic.topicId == topicId).scalar()
        try:
            exist = self.db.query(Likes).filter(Likes.topicId == topicId,
                                                Likes.userId == userId).one()  # 查找话题-用户点赞表，查看用户是否已经就该话题点过赞
            if exist:  # 该用户已对改话题点过赞
                retjson['code'] = '400'
                response = dict(
                likrnumber=self.db.query(Topic.likeNumber).filter(Topic.topicId == topicId).one(),
                name='点赞数',
                reply='不能重复点赞')
                retdata.append(response)
                retjson['content'] = retdata

        except NoResultFound:  # 未点过赞，可以点赞
            lnumber += 1
            like = Likes(
                topicId=topicId,
                userId=userId)
            self.db.query(Topic).filter(Topic.topicId == topicId).update({"likeNumber": lnumber})  # 更新
            self.db.merge(like)  # 在话题-用户表中加入改项
            try:
                self.db.commit()  # 修改后一定要commit更新数据库
            except Exception, e:
                self.db.rollback()
                retjson['code'] = 400
                retjson['content'] = "store data wrong!Try again"
            response = dict(
                likenumber=self.db.query(Topic.likeNumber).filter(Topic.topicId == topicId).one(),
                name="点赞数",
                reply='点赞成功')
            retdata.append(response)
            retjson['content'] = retdata

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))


class LikeComment(BaseHandler):  #  给讨论点赞

    def post(self):
        comId = self.get_argument('commentId',default='unsolved')  # 讨论名
        usId = self.get_argument('userId',default='unsolved')  # 用户名
        result = self.db.query(Comment.likeNumber).filter(comId == Comment.commentId).one() # comment like number
        clnumber = result.likeNumber
        retjson = {'code': '404', 'content': 'none'}
        retdata = []  # list array
        try:
            exist = self.db.query(CommentLike).filter(CommentLike.commentId == comId, usId == CommentLike.userId).one()  # 查找评论-用户点赞表，查看用户是否已经就该话题点过赞
            if exist:  # 该用户已对改话题点过赞
                retjson['code'] = '400'
                response = dict(
                    number=self.db.query(Comment.likeNumber).filter(Comment.commentId==comId).one(),
                    name="点赞数",
                    reply='不能重复点赞')
                retdata.append(response)
                retjson['content'] = retdata

        except NoResultFound:  # 未点过赞，可以点赞
            clnumber += 1
            clike = CommentLike(
                commentId=comId,
                userId=usId)
            self.db.query(Comment).filter(Comment.commentId==comId).update({"likeNumber": clnumber})  # 更新
            self.db.merge(clike)  # 在话题-用户表中加入改项
            try:
                self.db.commit()  # 修改后一定要commit更新数据库
                response = dict(
                number=self.db.query(Comment.likeNumber).filter(Comment.commentId==comId).one(),
                name="点赞数",
                reply='点赞成功')
                retdata.append(response)
                retjson['content'] = retdata
            except Exception, e:
                self.db.rollback()
                retjson['code'] = 400
                retjson['content'] = "store data wrong!Try again"


        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
