#!/usr/bin/env python
# coding:utf-8
# @Date    : 2015-12-8 12:46:36
# @Author  : jerry.liangj@qq.com
import tornado.web
import datetime
import json, urllib
from tornado.httpclient import HTTPRequest, HTTPClient
from config import UUID, EMPTYROOM_API_URL

class NewGetHandler(tornado.web.RequestHandler):
    def get(self, page=""):
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        tomorrow = (now + delta).strftime('%Y-%m-%d')
        self.render("newEmptyRoom.html", today=today, tomorrow=tomorrow)
    def post(self):
        ret = {'code':200, 'content':''}
        API_URL = EMPTYROOM_API_URL
        uuid = UUID
        try:
            url = self.get_argument("url", None)
            method = self.get_argument("method", None)
            data = self.get_argument("data", None)
            par = {
                "url":url,
                "uuid":uuid,
                "method":method,
                "data":data
            }
            if not (url and method):
                ret['code'] = 400
                ret['content'] = u'参数缺少'
            else:
                client = HTTPClient()
                request = HTTPRequest(
                    url=API_URL,
                    method="POST",
                    body=urllib.urlencode(par)
                    )
                response = client.fetch(request)
                content = json.loads(response.body)
                ret['content'] = content['content']
        except Exception, e:
            print str(e)
            ret['code'] = 500
            ret['content'] = u'系统错误'
        self.write(ret)