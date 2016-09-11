# -*- coding=utf-8 -*-
'''
Created on Aug 31, 2016

@author: corvo
'''

from ..Basehandler import BaseHandler
from datetime import datetime

class GetTimeListHandler(BaseHandler):
    """
     返回当前可用的时间列表
    """
    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET,POST')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)
        
    def post(self):
        retjson = {'code':200, 'content':''}

        now     = datetime.now()
        hour    = int(now.strftime("%H"))   # 当前小时
        minute  = int(now.strftime("%M"))   # 当前分钟
    
        content = ['12:20~12:40', '17:40~18:00']     # 11:30 之前均为当天快递

        if hour >= 11 and minute > 30:               # 11:30 ~ 17:00
            content = ['17:40~18:00', '次日12:20~12:40']

        if hour >= 17:                               # 17点以后
            content = ['次日12:20~12:40', '次日17:40~18:00']

        retjson['content'] = content
        self.write_back(retjson)
