#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from sqlalchemy import Column, Integer, Boolean, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship,backref
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

class Topics(Base):
	__tablename__="Topics"

	id=Column(Integer,nullable=False,primary_key=True)
	content=Column(VARCHAR(256))
	time=Column(VARCHAR(15),unique=True)

class Comments(Base):
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
    introduce   = Column(VARCHAR(256))
    detailurl   = Column(VARCHAR(256))
    user        = Column(VARCHAR(256))
    association = Column(VARCHAR(256))
    isvalid     = Column(Boolean(),default=True)
    ishot       = Column(Boolean(),default=True)

    def __str__(self):
        return 'title:{t}\t| association:{a}\t| start:{s}\t| end:{e}'\
            .format(t=self.title,a=self.association,s=self.starttime,e=self.endtime)

class ActivCommitUser(Base):
    __tablename__="ActivCommitUser"

    id          = Column(Integer,nullable=False,primary_key=True)
    user        = Column(VARCHAR(256))  # 用户
    password    = Column(VARCHAR(256))  # 密码
    association = Column(VARCHAR(256))  # 社团
    cookie      = Column(VARCHAR(256))  # cookie
    latestLogin = Column(DateTime())    # 上次登录时间
    login_fail_time = Column(Integer)   # 登录失败次数
    isvalid     = Column(Boolean(),default=True)  # 发布活动是否按照基本法




