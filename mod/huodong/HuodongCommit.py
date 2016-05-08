__author__ = 'multiangle'

import time,datetime

from tornado.httpclient import HTTPRequest, HTTPClient
from tornado.httputil import url_concat

from ..Basehandler import BaseHandler
from ..databases.tables import ActivCommitUser,Activity
from ..return_code_config import codeTable

class HuodongCommit(BaseHandler):

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

    def post(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')

        # check if cookie exists
        try:
            request_cookie = self.get_secure_cookie('ActivityCommitter').decode('utf8')
        except:
            retjson['code'] = 302
            retjson['content'] = codeTable[302]
            self.write_back(retjson)
            return

        # if the cookie is correct
        try:
            matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.cookie == request_cookie).one()
        except:
            retjson['code'] = 302
            retjson['content'] = codeTable[302]
            self.write_back(retjson)
            return

        # if the argument is enough
        try:
            start_time  = self.get_argument('start_time')
            end_time    = self.get_argument('end_time')
            title       = self.get_argument('title')
            introduce   = self.get_argument('introduce')
            detail_url  = self.get_argument('detail_url',None)
        except:
            retjson['code'] = 300
            retjson['content'] = codeTable[300]
            self.write_back(retjson)
            return

        # if the argument is correct
        try:
            s = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
            e = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
            if s>e :
                retjson['code'] = 409
                retjson['content'] = codeTable[409]
                self.write_back(retjson)
                return
        except:
            retjson['code'] = 409
            retjson['content'] = codeTable[409]
            self.write_back(retjson)
            return

        activity = Activity(
            committime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            starttime   = start_time,
            endtime     = end_time,
            title       = title,
            introduce   = introduce,
            detailurl   = detail_url,
            user        = matched_user.user,
            association = matched_user.association,
            isvalid     = True,
            ishot       = True
        )
        self.db.add(activity)
        self.db.commit()
        self.write_back(retjson)
