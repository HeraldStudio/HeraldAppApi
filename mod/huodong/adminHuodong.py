# -*- coding: utf-8 -*-
# @Date    : 2016/12/2  16:21
# @Author  : 490949611@qq.com
from ..Basehandler import BaseHandler
from mod.huodong.HuodongCommit import HuoException
from ..return_code_config import codeTable
from ..databases.tables import Activity
from ..databases.tables import ActivCommitUser
from sqlalchemy.orm.exc import NoResultFound

class AdminHuodong(BaseHandler):
    def get(self):
        # retjson = {'code':200,'content':''}
        # try:
        #     datas = self.db.query(Activity).order_by(Activity.starttime).all()
        #     ret_data = []
        #     for item in datas:
        #         temp = dict(
        #             id          = item.id,
        #             title       = item.title,
        #             location    = item.location,
        #             activity_time = item.activitytime,
        #             association = item.association,
        #             introduction= item.introduce,
        #             pic_url     = item.picurl,
        #             detail_url  = item.detailurl,
        #             start_time  = item.starttime.strftime("%Y-%m-%d"),
        #             end_time    = item.endtime.strftime("%Y-%m-%d"),
        #             if_valid    = item.isvalid,
        #             if_hot      = item.ishot
        #         )
        #         ret_data.append(temp)
        #     retjson['content'] = ret_data
        # except Exception,e:
        #     retjson['code'] = 500
        #     retjson['content'] = str(e)
        # self.write_back(retjson)
        self.render('HuoAdmin.html')

    def post(self):
        retjson = {'code':200,'content':'ok'}
        activityId = self.get_argument('activityId',default=None)
        handle = self.get_argument('handle',default=None)
        if not (activityId and handle):
                retjson['code'] = 300
                retjson['content'] = codeTable[300]

        # check if cookie exists
        request_cookie = self.get_secure_cookie('ActivityCommitter')
        if request_cookie:
        # if the cookie is correct
            try:
                matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.cookie == request_cookie).one()
                if int(matched_user.level) != 1:
                    retjson['code'] = 410
                    retjson['content'] = codeTable[410]
                else:
                    try:
                        activity = self.db.query(Activity).filter(Activity.id == int(activityId)).one()
                        activity_status = int(activity.isvalid)
                        if not (activity_status ^ int(handle)):
                            retjson['code'] = 412
                            retjson['content'] = codeTable[412]
                        else:
                            activity.isvalid = int(handle)
                            self.db.commit()
                    except Exception,e:
                        print str(e)
                        retjson['code'] = 409
                        retjson['content'] = codeTable[409]
            except Exception,e:
                    retjson['code'] = 500
                    retjson['content'] = codeTable[500]
        else:
            retjson['code'] = 302
            retjson['content'] = codeTable[302]
        self.write(retjson)


