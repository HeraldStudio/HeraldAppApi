# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import json
import traceback
import urllib
from ..Basehandler import BaseHandler
from tornado.httpclient import HTTPRequest, HTTPClient
from tornado.httputil import url_concat
from refreshCookie import refreshCookie

class YuyueHandler(BaseHandler):

    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def get(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)


    def getData(self,url,method,data,cookie):
        try:
            client = HTTPClient()
            request = HTTPRequest(
                    url,
                    method=method,
                    headers={
                        'Cookie':cookie
                    }
                )
            if data and method=="GET":
                data = json.loads(data)
                url = url_concat(url,data)
                request.url = url
            elif data and method=="POST":
                data = json.loads(data)
                data = urllib.urlencode(data)
                request.body = data
            # print request.url
            response = client.fetch(request)
            return response.body
        except Exception,e:
            # print str(e)
            return None

    def post(self):
        retjson = {'code':200,'content':''}
        user = self.get_current_user()
        if not user:
            retjson['code'] = 400
            retjson['content'] = u'请先登录'
        else:
            try:
                url = self.get_argument('url',None)
                method = self.get_argument('method',None)
                data = self.get_argument('data',None)

                if not (url and method):
                    retjson['code'] = 400
                    retjson['content'] = u'缺少必要参数'
                else:
                    state,cookie = refreshCookie(self.db,user)
                    if state:
                        response = self.getData(url,method,data,cookie)
                        if response:
                            retjson['content'] = json.loads(response)
                        else:
                            retjson['code'] = 500
                            retjson['content'] = u'请求失败'
                    else:
                        retjson['code'] = 501
                        retjson['content'] = u'系统错误'
            except ValueError:
                retjson['code'] = 200
                retjson['content'] = response
            except:
                # print traceback.print_exc()
                retjson['code'] = 500
                retjson['content'] = u'系统错误'
        self.set_header('Access-Control-Allow-Methods','GET,POST')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

