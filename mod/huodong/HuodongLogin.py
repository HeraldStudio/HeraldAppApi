# -*- coding: utf-8 -*-
__author__ = 'multiangle'

import time,datetime

from ..Basehandler import BaseHandler
from ..databases.tables import ActivCommitUser
from ..return_code_config import codeTable

class HuodongLogin(BaseHandler):
    def get(self):
        self.render('HuoLogin.html')

    def post(self):
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')

        retjson = {'code':200}

        # if the argument is enough
        try:
            user = self.get_argument('user')
            password = self.get_argument('password')
        except Exception as e:
            retjson['code'] = 300
            retjson['content'] = codeTable[300]
            self.write_back(retjson)
            return

        # if the user exists
        try:
            matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.user==user).one()
        except:
            retjson['code'] = 301
            retjson['content'] = codeTable[301]
            self.write_back(retjson)
            return

        if matched_user.login_fail_time == None :
            matched_user.login_fail_time = 0

        MAX_FAIL_TIME = 10
        BANNED_LOGIN_TIME = 10*60 # seconds
        if matched_user.login_fail_time>= MAX_FAIL_TIME :
            # if the user is banned
            latestLogin_timestamp = time.mktime(matched_user.latestLogin.timetuple())
            if latestLogin_timestamp+BANNED_LOGIN_TIME<int(time.time()) :
                # not banned now
                matched_user.login_fail_time = 0
            else:
                # still banned now
                retjson['code'] = 400
                retjson['content'] = '您登录错误次数太多，请稍后再试'
                self.db.commit()
                self.write_back(retjson)
                return

        # if the password is correct
        if password!=matched_user.password :
            matched_user.login_fail_time += 1
            matched_user.latestLogin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            retjson['code'] = 400
            retjson['content'] = codeTable[400]
            self.db.commit()
            self.write_back(retjson)
            return

        matched_user.login_fail_time = 0
        matched_user.latestLogin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cookie_value = matched_user.user + '_' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        matched_user.cookie = cookie_value
        self.set_secure_cookie('ActivityCommitter',cookie_value,expires_days=2)
        self.db.commit()
        self.write_back(retjson)