__author__ = 'multiangle'

import datetime


from ..Basehandler import BaseHandler
from ..databases.tables import ActivCommitUser, Activity
from ..return_code_config import codeTable
from sqlalchemy.orm.exc import NoResultFound

class HuoException(RuntimeError):
    def __init__(self, code):
        self.code = code

class HuodongCommit(BaseHandler):
    def get(self):
        request_cookie = self.get_secure_cookie('ActivityCommitter')
        state = 1
        matched_user = None
        if request_cookie:
            try:
                matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.cookie == request_cookie).one()
            except NoResultFound:
                state = 0
        else:
            state = 0
        if state==1:
            self.render('commit.html')
        else:
            self.redirect('./login')

    def post(self):
        retjson = {'code':200,'content':'ok'}
        self.set_header('Access-Control-Allow-Methods','GET')
        self.set_header('Access-Control-Allow-Headers','token')

        try:
            # if the argument is enough
            start_time  = self.get_argument('start_time',default=None)
            end_time    = self.get_argument('end_time',default=None)
            activity_time = self.get_argument('activity_time',default=None)
            title       = self.get_argument('title',default=None)
            location    = self.get_argument('location',default=None)
            introduce   = self.get_argument('introduce',default=None)
            is_hot      = self.get_argument('is_hot',default=False)
            picurl      = self.get_argument('picurl',default=None)
            detail_url  = self.get_argument('detail_url',None)
            if not(start_time and end_time and title and introduce and location):
                retjson['code'] = 300
                retjson['content'] = codeTable[300]
            elif  len(introduce)>200:
                retjson['code'] = 411
                retjson['content'] = codeTable[411]
            else:
                # if the argument is correct
                try:
                    s = datetime.datetime.strptime(start_time,"%Y-%m-%d")
                    e = datetime.datetime.strptime(end_time,"%Y-%m-%d")
                    if s>e :
                        raise HuoException(409)
                except:
                    raise HuoException(409)

                # check if cookie exists
                request_cookie = self.get_secure_cookie('ActivityCommitter')
                if request_cookie:
                    # if the cookie is correct
                    matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.cookie == request_cookie).one()
                    # insert the data
                    activity = Activity(
                        committime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        starttime   = start_time,
                        endtime     = end_time,
                        activitytime= activity_time,
                        title       = title,
                        picurl      = picurl,
                        location    = location,
                        introduce   = introduce,
                        detailurl   = detail_url,
                        user        = matched_user.user,
                        association = matched_user.association,
                        isvalid     = False,
                        ishot       = is_hot
                    )
                    self.db.add(activity)
                    self.db.commit()
                else:
                    raise HuoException(302)
        except HuoException,e:
            retjson['code'] = e.code
            retjson['content'] = codeTable[e.code]
        except NoResultFound:
            retjson['code'] = 302
            retjson['content'] = codeTable[302]
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = str(e)
        self.write_back(retjson)
