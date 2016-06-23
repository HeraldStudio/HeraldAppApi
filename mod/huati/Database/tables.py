# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey,DateTime
from sqlalchemy.types import CHAR, Integer, VARCHAR
import sys
reload(sys)
from models import Base


# 每个类对应一个表
class User(Base): # 用户表
    __tablename__ = 'user'

    phone = Column(VARCHAR(11), nullable=False, primary_key=True)
    password = Column(VARCHAR(32), nullable=False) # 密码
    name = Column(VARCHAR(64))
    cardnum = Column(VARCHAR(9), nullable=False, unique=True)
    card_password = Column(VARCHAR(64), nullable=False)   # 统一身份认证密码
    salt = Column(VARCHAR(64))


class Likes(Base): # 点赞表
    __tablename__ = 'likes'

    topicId = Column(Integer,primary_key=True)
    userId = Column(Integer)

class Topic(Base): # 话题表
    __tablename__ = 'topic'

    topicId = Column(Integer, nullable=False, primary_key=True, unique=True)
    name = Column(VARCHAR(255))
    content = Column(VARCHAR(255))
    commentNumber = Column(Integer)
    likeNumber = Column(Integer)
    startTime = Column(DateTime())
    endTime = Column(DateTime())


class Comment(Base):  # 评论表
    __tablename__ = 'comments'

    commentId = Column(Integer, nullable=False, primary_key=True, unique=True)
    topicId = Column(Integer)
    userId = Column(Integer)
    content = Column(VARCHAR(255))
    time = Column(DateTime())
    likeNumber = Column(Integer)


class CommentLike(Base):   # 评论点赞表
    __tablename__ = 'commentlike'

    commentId = Column(Integer,primary_key=True)
    userId = Column(Integer)
