#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

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

	id		= Column(Integer,nullable=False,primary_key=True)
	topicid	= Column(Integer,ForeignKey('Topics.id', ondelete='CASCADE'))
	content	= Column(VARCHAR(256))
	zans	= Column(Integer,default=0)
	time 	= Column(VARCHAR(15),unique=True)
	phone 	= Column(VARCHAR(64),ForeignKey('Users.phone', ondelete='CASCADE'))

class RUsersComments(Base):
 	__tablename__="RUsersComments"

 	id			= Column(Integer,nullable=False,primary_key=True)
 	commentid	= Column(Integer,ForeignKey('Comments.id', ondelete='CASCADE'))
 	phone 		= Column(VARCHAR(64),ForeignKey('Users.phone', ondelete='CASCADE'))
 	zans 		= Column(Integer,default=0)

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




