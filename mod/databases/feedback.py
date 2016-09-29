#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com

from sqlalchemy import Column, String, Integer 
from db import engine, Base

#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()

class FeedBack(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(String(64), nullable=False)
    user = Column(Integer)
    response = Column(String(4096))
    state = Column(Integer)

class WechatFeedBack(Base):
    __tablename__ = 'wechat_feedback'
    id = Column(Integer, primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(String(64), nullable=False)
    user = Column(Integer)
    response = Column(String(4096))
    state = Column(Integer)


if __name__ == '__main__':
    Base.metadata.create_all(engine)