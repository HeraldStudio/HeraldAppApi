#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from tables import  Access_Token,Users,Topics,Comments,RUsersComments,Activity,ActivCommitUser,Express,ExpressModify,ExpressAdmin
from feedback import FeedBack, WechatFeedBack
from db import engine, Base

Base.metadata.create_all(engine) #create all of Class which belonged to Base Class
