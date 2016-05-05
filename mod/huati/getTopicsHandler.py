# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2016-03-11 14:25:05
# @Author  : qianxin@live.cn

import hashlib
import random
import string
import urllib

import uuid
import time,json
from ..databases.tables import Users,Comments
from ..Basehandler import BaseHandler
from tornado.httpclient import HTTPRequest, HTTPClient,HTTPError
from sqlalchemy.exc import IntegrityError
from config import *
import traceback

class GetTopicsHandler(BaseHandler):

    def post(self):
        ret = {'code':200,'content':u''}
        tempNum=20*(pageNo-1);
        topicsArray = self.db.execute("select top 20 * from topics where (id not in (select top %d * from topics order order by time ASC)order by time ASC "%tempNum).fetchall()
        #select top xx * 
        #from topics 
        #where (id not in (
        	#select top xx * 
        	#from topics 
        	#order by zans DESC,time ASC )
		#order by zans DESC,time ASC  

        self.write_back(ret)