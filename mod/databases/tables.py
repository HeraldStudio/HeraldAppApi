#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, VARCHAR,ForeignKey
from sqlalchemy.orm import relationship,backref
from db import Base

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


