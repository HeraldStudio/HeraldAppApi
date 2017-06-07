#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
#sys.setdefaultencoding( "utf-8" )

from sqlalchemy import Column, Integer, Boolean, VARCHAR, DateTime, ForeignKey
from db import Base
import datetime

class Users(Base):
    __tablename__ = 'Users'

    phone = Column(VARCHAR(11),nullable=False,primary_key=True)
    password = Column(VARCHAR(32),nullable=False)
    name = Column(VARCHAR(64))
    cardnum = Column(VARCHAR(9),nullable=False,unique=True)
    card_password = Column(VARCHAR(64),nullable=False)
    salt = Column(VARCHAR(64))

class Access_Token(Base):
    __tablename__ = "Token"

    phone = Column(VARCHAR(64),ForeignKey('Users.phone', ondelete='CASCADE'))
    token = Column(VARCHAR(64),nullable=False,primary_key=True)
    cookie = Column(VARCHAR(256))
    last_time = Column(VARCHAR(15))
    ip = Column(VARCHAR(32))

class Topics(Base):    # 话题表
    __tablename__="Topics"

    id=Column(Integer,nullable=False,primary_key=True)
    content=Column(VARCHAR(256))
    time=Column(VARCHAR(15),unique=True)

class Comments(Base):   # 评论表
    __tablename__="Comments"

    id        = Column(Integer,nullable=False,primary_key=True)
    topicid    = Column(Integer,ForeignKey('Topics.id', ondelete='CASCADE'))
    content    = Column(VARCHAR(256))
    zans    = Column(Integer,default=0)
    time     = Column(VARCHAR(15),unique=True)
    phone     = Column(VARCHAR(64),ForeignKey('Users.phone', ondelete='CASCADE'))

class RUsersComments(Base):
    __tablename__="RUsersComments"

    id            = Column(Integer,nullable=False,primary_key=True)
    commentid    = Column(Integer,ForeignKey('Comments.id', ondelete='CASCADE'))
    phone         = Column(VARCHAR(64),ForeignKey('Users.phone', ondelete='CASCADE'))
    zans         = Column(Integer,default=0)

class Activity(Base):
    __tablename__="Activity"

    id          = Column(Integer,nullable=False,primary_key=True)
    committime  = Column(DateTime(),default=datetime.datetime.now())
    starttime   = Column(DateTime())
    endtime     = Column(DateTime())
    title       = Column(VARCHAR(128))
    picurl      = Column(VARCHAR(128))
    location    = Column(VARCHAR(128))
    activitytime= Column(VARCHAR(32))
    introduce   = Column(VARCHAR(128))
    detailurl   = Column(VARCHAR(128))
    user        = Column(VARCHAR(64))
    association = Column(VARCHAR(128))
    isvalid     = Column(Boolean(),default=True)
    ishot       = Column(Boolean(),default=True)

    def __str__(self):
        return 'title:{t}\t| association:{a}\t| start:{s}\t| end:{e}'\
            .format(t=self.title,a=self.association,s=self.starttime,e=self.endtime)

class ActivCommitUser(Base):
    __tablename__="ActivCommitUser"

    id          = Column(Integer,nullable=False,primary_key=True)
    user        = Column(VARCHAR(64))  # 用户
    password    = Column(VARCHAR(64))  # 密码
    association = Column(VARCHAR(128))  # 社团
    cookie      = Column(VARCHAR(128))  # cookie
    latestLogin = Column(DateTime())    # 上次登录时间
    login_fail_time = Column(Integer)   # 登录失败次数
    isvalid     = Column(Boolean(),default=True)  # 发布活动是否按照基本法
    level       = Column(Integer,default=3) #user权限（1为普通管理员，2为活动提交者，3是闲杂人等）


# 快递模块
class Express(Base):
    __tablename__ = "express_data"
    id            = Column(Integer, nullable    = False, primary_key = True)
    cardnum       = Column(VARCHAR(9), nullable = False) # 一卡通号, 防止恶意
    #uuid          = Column(VARCHAR(64))                                     # uuid校验
    sms           = Column(VARCHAR(256))                                     # 快递短信
    user          = Column(VARCHAR(64))                                      # 客户姓名
    phone         = Column(VARCHAR(64))                                      # 客户联系电话
    dest          = Column(VARCHAR(64))                                      # 客户取快递地点
    arrival       = Column(VARCHAR(64))                                      # 客户取快递时间段
    locate        = Column(VARCHAR(64))                                      # 快件所在地(东门/南门)
    weight        = Column(VARCHAR(64))                                      # 快件重量
    submittime    = Column(DateTime())                                       # 信息提交时间
    receiving    = Column(Boolean, unique = False, default = False)         # 是否有人接单
    finish        = Column(Boolean, unique = False, default = False)         # 已经交到用户手中, 本次代取结束

class ExpressModify(Base):
    """
        保存每个管理员的修改内容
    """
    __tablename__ = "express_modify"
    id = Column(Integer, nullable = False, primary_key = True)
    superuser = Column(VARCHAR(9), nullable=False)      # 管理员id
    modify = Column(VARCHAR(2048))                      # 管理员修改内容
    modifytime = Column(DateTime())                     # 信息提交时间

class ExpressAdmin(Base):
    """
    快递模块管理员
    """
    __tablename__ = "express_admin"
    id = Column(Integer,nullable = False, primary_key = True)
    name = Column(VARCHAR(32), nullable = False)
    password = Column(VARCHAR(32), nullable = False)
    token = Column(VARCHAR(64))


# 话题模块
class Topic(Base):  # 话题表
    __tablename__ = 'Topic'

    id = Column(Integer, nullable=False, primary_key=True, unique=True)
    name = Column(VARCHAR(64), nullable=False)  # 话题名
    content = Column(VARCHAR(256), nullable=False)  # 话题内容
    commentN = Column(Integer, nullable=False, default=0)  # 评论数
    readN = Column(Integer, default=0, nullable=False)  # 浏览人数
    startT = Column(DateTime())  # 开始时间
    valid = Column(Boolean, default=True, nullable=False)


class Tcomment(Base):  # 评论表
    __tablename__ = 'Tcomment'

    id = Column(Integer, nullable=False, primary_key=True, unique=True)
    topicid = Column(Integer, ForeignKey('Topic.id', onupdate='CASCADE'), nullable=False)  # 话题id
    cardnum = Column(VARCHAR(9), ForeignKey('Users.cardnum', onupdate='CASCADE'))  # 评论人一卡通号
    content = Column(VARCHAR(255), nullable=False)
    commentT = Column(DateTime())  # 评论时间
    likeN = Column(Integer, default=0)  # 点赞数
    quote = Column(Integer, ForeignKey('Tcomment.id', onupdate='CASCADE'), default=1)   # 评论引用，为评论Id，作为一级评论的回复
    anonymous = Column(Boolean, default=False, nullable=False)  # 判断是否匿名
    valid = Column(Boolean, default=True, nullable=False)


class Tpraise(Base):  # 话题点赞表
    __tablename__ = 'Tpraise'
    id = Column(Integer, nullable=False, primary_key=True)
    cardnum = Column(VARCHAR(9), ForeignKey('Users.cardnum', onupdate='CASCADE'))  # 评论人一卡通号
    commentid = Column(Integer, ForeignKey('Tcomment.id', onupdate='CASCADE'), nullable=False)
    paraseT = Column(DateTime())  # 评论时间
    valid = Column(Boolean, default=True, nullable=False)

class TopicAdmin(Base):
    """
    快递模块管理员
    """
    __tablename__ = "topic_admin"
    id = Column(Integer,nullable = False, primary_key = True)
    name = Column(VARCHAR(32), nullable = False)
    password = Column(VARCHAR(32), nullable = False)
    token = Column(VARCHAR(64))

class SlideViews(Base):
    """
    轮播图模块
    """
    __tablename__ = 'slideviews'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(1024))
    imageurl = Column(VARCHAR(1024))
    url = Column(VARCHAR(1024))
    begin_time = Column(DateTime())
    end_time = Column(DateTime())
    #key = Column(VARCHAR(1024))
    hit_count = Column(Integer)  # 轮播推送到的次数

class PushMessage(Base):
    __tablename__ = 'pushmessages'
    id = Column(Integer, primary_key=True)
    content = Column(VARCHAR(1024))
    url = Column(VARCHAR(1024))
    schoolnum = Column(VARCHAR(1024))  # 用于针对某一特定用户的推送
    versiontype = Column(VARCHAR(1024))  # 用于针对某一特定平台的推送
    priority = Column(Integer)  # 用于指定推送匹配的优先级顺序
    hit_count = Column(Integer)  # 推送匹配到的次数

class DayLogAnalyze(Base):
    """
    每日日志重要信息记录
    """
    __tablename__     = "DayLogAnalyze"
    id                = Column(Integer       , nullable = False                       , primary_key = True)
    date              = Column(VARCHAR(32)   , nullable = False) # 表项名称access_api.log-date
    api_order         = Column(VARCHAR(10800) , nullable = False) # 该日Api请求数目(保留前20)
    ip_order          = Column(VARCHAR(1080) , nullable = False) # 该日ip请求数目(保留前30)
    every_hour_count  = Column(VARCHAR(1024) , nullable = False) # 该日每小时访问量
    device_distribute = Column(VARCHAR(1080) , nullable = False) # 该日发送请求的设备分布
    call_count        = Column(Integer       , nullable = False) # 该日请求次数
    ios_version       = Column(VARCHAR(1080) , nullable = True)  # ios设备版本分布
    android_version   = Column(VARCHAR(1080) , nullable = True)  # android设备版本分布

class Admin(Base):
    __tablename__ = 'admin'
    id  = Column(Integer,primary_key=True)
    name = Column(VARCHAR(200),nullable=False)
    privilege = Column(Integer,nullable=False)
    pwd = Column(VARCHAR(64),nullable=False)
    salt = Column(VARCHAR(64),nullable=False)
