# -*- coding: utf-8 -*-
#!/usr/bin/env python

# @Date    : 2016-05-13 11:20:05
# @Author  : jerry.liangj@qq.com

import tornado.web
import tornado.gen

class biaobaiStaticHandler(tornado.web.RequestHandler):

    def get(self):
    	url = "127.0.0.1:7000"
    	day = 19
    	start_hour = -1
    	end_hour = 24
        self.render("biaobai.html",url=url,day=day,start_hour=start_hour,end_hour=end_hour)

class InStaticHandler(tornado.web.RequestHandler):
	
	def get(self):
		self.render("enter.html")