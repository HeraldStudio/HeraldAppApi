__author__ = 'multiangle'
# -*- coding: utf-8 -*-

import time,datetime

from ..Basehandler import BaseHandler
from ..databases.tables import Activity
from sqlalchemy import desc,and_
from tornado.httpclient import HTTPRequest, HTTPClient
from tornado.httputil import url_concat

class getHuodong(BaseHandler):

    # there are 2 argument in request, type and page. for example :
    # .1 : .../huodong/get
    # .2 : .../huodong/get?page=0
    # .3 : .../huodong/get?type=hot
    # .4 : .../huodong/get?page=0&type=hot

    def options(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def get(self):
        retjson = {'code':200}

        type = self.get_argument('type',default='alive')
        if type!='hot':
            type='alive'

        page = int(self.get_argument('page',default=1))
        if page == 0 :
            page=1

        if type=='alive':
            data = self.db.query(Activity).filter(Activity.isvalid == True).order_by(desc(Activity.committime)).all()
        else:
            data = self.db.query(Activity)\
                .filter(and_(Activity.isvalid == True, Activity.ishot == True))\
                .order_by(desc(Activity.committime))\
                .all()

        THREADS_NUM_EACHPAGE = 10
        start_index = (page-1)*THREADS_NUM_EACHPAGE
        end_index = page*THREADS_NUM_EACHPAGE-1
        data = data[min(start_index,data.__len__()):min(end_index,data.__len__())]

        ret_data = []
        for item in data:
            temp = dict(
                title       = item.title,
                association = item.association,
                introduction= item.introduce,
                detail_url  = item.detailurl,
                start_time  = item.starttime.strftime("%Y-%m-%d %H:%M:%S"),
                end_time    = item.endtime.strftime("%Y-%m-%d %H:%M:%S")
            )
            ret_data.append(temp)
        retjson['data'] = ret_data
        # print(ret_data)
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)

    def post(self):
        retjson = {'code':200}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')
        self.write_back(retjson)