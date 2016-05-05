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

class GetCommentsHandler(BaseHandler):
    def get(self):
        ret = {'code':200,'content':'ok'}
        self.write(json.dumps(ret,ensure_ascii=False, indent=2))

    def post(self):
        retjson = {'code':200,'content':'ok'}
        topicid =self.get_argument('topic_id',None)
        tempNum=20*(pageNo-1);
        commentsArray = self.db.execute("select top 20 * from comments where (id not in (select top %d * from comments where topicid=%s order order by zans DESC,time ASC)order by zans DESC,time ASC "%(tempNum,topicid)).fetchall()
        #select top xx * 
        #from comments 
        #where (id not in (
        	#select top xx * 
        	#from comments 
        	#where topicid=topicid order by zans DESC,time ASC)
		#order by zans DESC,time ASC  

        self.write_back(retjson)