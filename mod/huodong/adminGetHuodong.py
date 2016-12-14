# -*- coding: utf-8 -*-
# @Date    : 2016/12/14  14:35
# @Author  : 490949611@qq.com
from ..Basehandler import BaseHandler
from mod.huodong.HuodongCommit import HuoException
from ..return_code_config import codeTable
from ..databases.tables import Activity
from ..databases.tables import ActivCommitUser
from sqlalchemy.orm.exc import NoResultFound

class AdminGetHuodong(BaseHandler):
    def get(self):
        retjson = {'code':200,'content':''}
        try:
            datas = self.db.query(Activity).order_by(Activity.starttime).all()
            ret_data = []
            for item in datas:
                temp = dict(
                    id          = item.id,
                    title       = item.title,
                    location    = item.location,
                    activity_time = item.activitytime,
                    association = item.association,
                    introduction= item.introduce,
                    pic_url     = item.picurl,
                    detail_url  = item.detailurl,
                    start_time  = item.starttime.strftime("%Y-%m-%d"),
                    end_time    = item.endtime.strftime("%Y-%m-%d"),
                    if_valid    = item.isvalid,
                    if_hot      = item.ishot
                )
                ret_data.append(temp)
            retjson['content'] = ret_data
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = str(e)
        self.write_back(retjson)
        self.render('HuoAdmin.html')
