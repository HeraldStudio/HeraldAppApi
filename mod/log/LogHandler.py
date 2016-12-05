#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: December 05, 2016
    Author: corvo
"""

import json

from sqlalchemy import desc
#import timestamp

from mod.Basehandler import BaseHandler

class LogHandler(BaseHandler):
    """
        本模块为日志分析后端模块, 预先分析好的日志先存储于数据库中, 
        使用时读取数据库中的json信息, 做简单处理后返回
    """

    def post(self):

        ask_code = self.get_argument('askcode', default='unsolved')
        print("hello world")
        print(ask_code)
        

