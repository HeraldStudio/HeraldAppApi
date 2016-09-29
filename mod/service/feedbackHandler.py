#!/usr/bin/env python
#coding:utf-8
# @Date    : 2015-12-8 12:46:36
# @Author  : jerry.liangj@qq.com
import tornado.web
import datetime
import json,urllib
from tornado.httpclient import HTTPRequest,HTTPClient
from mod.databases.feedback import WechatFeedBack,FeedBack
from time import time,localtime, strftime

class FeedBackHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    def get(self):
        number = self.get_argument("cardnum",default='0')
        user = self.get_secure_cookie("feedbackuser")
        if not user:
            self.set_secure_cookie("feedbackuser",number)
        self.render('feedback.html')

    def post(self):
        ret = {'code':200,'content':u'小猴收到啦~感谢您的反馈'}
        content = self.get_argument('content',None)
        cardnum = self.get_argument('cardnum',default = None)
        number = self.get_secure_cookie("feedbackuser")
        if not content:
            ret['code'] = 400
            ret['content'] = u'反馈内容不能为空哦~'
        if not number and not cardnum:
            ret['code'] = 400
            ret['content'] = u'请先登录~'
        else:
            now = strftime("%Y-%m-%d %H:%M:%S",localtime(time()))
            if cardnum:
                feedback = FeedBack(text=content,date=now,user=cardnum)
            else:
                feedback = WechatFeedBack(text=content,date=now,user=number)
            try:
                self.db.add(feedback)
                self.db.commit()
            except Exception,e:
                self.db.rollback()
                ret['code'] = 500
                ret['content'] = u'系统错误'
        self.write(json.dumps(ret,ensure_ascii=False, indent=2))

class FeedBackSuccessHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('feedback_success.html')

class FeedBackDetailsHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    def get(self):
        try:
            data = self.db.query(WechatFeedBack).filter(WechatFeedBack.response!=None).order_by(WechatFeedBack.date.desc()).all()
            number = self.get_secure_cookie("feedbackuser")
            mydata = self.db.query(WechatFeedBack).filter(WechatFeedBack.user==number).order_by(WechatFeedBack.date.desc()).all()
        except Exception,e:
            data = []
            mydata = []
        self.render('feedback_details.html',data = data,mydata = mydata)