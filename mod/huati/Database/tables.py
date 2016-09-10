# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey,DateTime
from sqlalchemy.types import CHAR, Integer, VARCHAR
import sys
reload(sys)
from models import Base


# 每个类对应一个表
class User(Base): # 用户表
    __tablename__ = 'User'

    phone = Column(VARCHAR(11), nullable=False, primary_key=True)
    password = Column(VARCHAR(32), nullable=False) # 密码
    name = Column(VARCHAR(64))
    cardnum = Column(VARCHAR(9), nullable=False, unique=True)
    card_password = Column(VARCHAR(64), nullable=False)   # 统一身份认证密码
    salt = Column(VARCHAR(64))


class Likes(Base): # 点赞表
    __tablename__ = 'Likes'

    topicId = Column(Integer, ForeignKey('Topic.topicId',  onupdate='CASCADE'), primary_key=True)
    user_phone = Column(VARCHAR(11), ForeignKey('User.phone',  onupdate='CASCADE'))

class Topic(Base): # 话题表
    __tablename__ = 'Topic'

    topicId = Column(Integer, nullable=False, primary_key=True, unique=True)
    name = Column(VARCHAR(255))
    content = Column(VARCHAR(255))
    sponsor = Column(VARCHAR(11), ForeignKey('User.phone',  onupdate='CASCADE'))
    comment_number = Column(Integer)
    like_number = Column(Integer, default=0)
    start_time = Column(VARCHAR(15))
    end_time = Column(VARCHAR(15))


class Comment(Base):  # 评论表
    __tablename__ = 'Comments'

    commentId = Column(Integer, nullable=False, primary_key=True, unique=True)
    topicId = Column(Integer, ForeignKey('Topic.topicId', onupdate='CASCADE'))
    user_phone = Column(VARCHAR(11), ForeignKey('User.phone', onupdate='CASCADE'))
    content = Column(VARCHAR(255))
    time = Column(VARCHAR(15))
    like_number = Column(Integer, default=0)


class CommentLike(Base):   # 评论点赞表
    __tablename__ = 'commentlike'

    commentId = Column(Integer, ForeignKey('Comments.commentId', onupdate='CASCADE'), primary_key=True)
    user_phone = Column(VARCHAR(11), ForeignKey('User.phone', onupdate='CASCADE'))