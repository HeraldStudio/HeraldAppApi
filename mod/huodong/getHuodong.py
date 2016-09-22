# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'multiangle'

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
    def get(self):
        retjson = {'code':200,'content':''}

        type = self.get_argument('type',default='alive')
        if type!='hot':
            type='alive'

        page = int(self.get_argument('page',default=0))
        if page == 0 :
            page=1
        THREADS_NUM_EACHPAGE = 10
        start_index = (page-1)*THREADS_NUM_EACHPAGE
        end_index = page*THREADS_NUM_EACHPAGE-1
        now = datetime.datetime.now()
        try:
            if type=='alive':
                data_valid = self.db.query(Activity).filter(Activity.isvalid == True,Activity.endtime>=now).order_by(Activity.starttime).all()
                data_invalid = self.db.query(Activity).filter(Activity.isvalid == True,Activity.endtime<now).order_by(Activity.starttime.desc()).all()
                data = (data_valid+data_invalid)[start_index:end_index]
            else:
                data = self.db.query(Activity)\
                    .filter(and_(Activity.isvalid == True, Activity.ishot == True,Activity.endtime>=now))\
                    .order_by(Activity.starttime)\
                    [start_index:end_index]

            ret_data = []
            for item in data:
                temp = dict(
                    title       = item.title,
                    location    = item.location,
                    activity_time = item.activitytime,
                    association = item.association,
                    introduction= item.introduce,
                    pic_url     = item.picurl,
                    detail_url  = item.detailurl,
                    start_time  = item.starttime.strftime("%Y-%m-%d"),
                    end_time    = item.endtime.strftime("%Y-%m-%d")
                )
                ret_data.append(temp)
            retjson['content'] = ret_data
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = str(e)
        # print(ret_data)
        self.write_back(retjson)
