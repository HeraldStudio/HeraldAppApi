# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import hashlib
import random
import string
import urllib

import uuid
import time,json
from ..databases.tables import Users,Access_Token
from ..Basehandler import BaseHandler
from tornado.httpclient import HTTPRequest, HTTPClient,HTTPError
from sqlalchemy.exc import IntegrityError
from config import *
import traceback

class RegisterHandler(BaseHandler):

    def post(self):
        ret = {'code':200,'content':u'注册成功'}
        phone = self.get_argument('phone',None)
        pwd = self.get_argument('password',None)
        cardnum = self.get_argument('cardnumber',None)
        card_pwd = self.get_argument('card_password',None)
        if not (cardnum and pwd and phone and card_pwd):
            ret['code'] = 400
            ret['content'] = u'参数不能为空'
        elif len(phone)!=11 or (not phone.isdigit()):
            ret['code'] = 402
            ret['content'] = u'手机号格式不正确'
        elif len(pwd) < 6:
                ret['code'] = 401
                ret['content'] = u'密码太短'
        else:
            try:
                state = 1
                cookie = ''
                client = HTTPClient()
                data = {
                    'username':cardnum,
                    'password':card_pwd
                }
                request = HTTPRequest(
                    LOGIN_URL,
                    method="POST",
                    body=urllib.urlencode(data),
                    validate_cert=False,
                    request_timeout=4
                )
                response = client.fetch(request)
                header = response.headers
                if 'Ssocookie' in header.keys():
                    headertemp = json.loads(header['Ssocookie'])
                    cookie = headertemp[1]['cookieName']+"="+headertemp[1]['cookieValue']
                    cookie += ";"+header['Set-Cookie'].split(";")[0]
                    salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                    pwd =  hashlib.md5(salt.join(pwd)).hexdigest()
                    user = Users(phone = phone,password = pwd,cardnum = cardnum,card_password = card_pwd,salt =salt)
                    self.db.add(user)
                    self.db.commit()
                else:
                    state = 0
                    ret['code'] = 400
                    ret['content'] = u'一卡通账号密码错误'
            except IntegrityError,e:#判断手机号是否已被注册
                    state = 0
                    ret['code'] = 403
                    ret['content'] = u'该手机号已被注册或一卡通号已绑定'
                    self.db.rollback()
            except:
                state = 0
                self.db.rollback()
                # print traceback.print_exc()
                ret['code'] = 500
                ret['content'] = u'系统错误'

            if state == 1:
                try:
                    token = uuid.uuid1()
                    access_token = Access_Token(phone = phone,token = token,cookie = cookie,last_time = int(time.time()))
                    self.db.add(access_token)
                    self.db.commit()
                    ret['content'] = str(token)
                except Exception,e:
                    # print str(e)
                    self.db.rollback()
                    ret['code'] = 500
                    ret['content'] = u'写入错误'
        self.write_back(ret)