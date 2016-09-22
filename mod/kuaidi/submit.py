# -*- coding=utf-8 -*-

"""
Created on Aug 4, 2016

@author: corvo
"""

from datetime import datetime,date,time

from ..Basehandler import BaseHandler
from sqlalchemy.orm.exc import NoResultFound
from mod.databases.tables import Express,Users
from ..return_code_config import generate_ret


class SubmitHandler(BaseHandler):
    """
    提交的去快递请求在此处理, 提交成功后将会返回unix时间戳
    目前每天最大下五单
    """
    def post(self):
        OneDayMaxCount = 5
        retjson = generate_ret('express',200)

        _user = self.get_current_user()
        _user_name = self.get_argument('user_name', default=None)
        _sms_txt = self.get_argument('sms_txt', default=None)
        _user_phone = self.get_argument('phone', default=None)
        _dest = self.get_argument('dest', default=None)
        _arrival = self.get_argument('arrival', default=None)
        _locate = self.get_argument('locate', default=None)
        _weight = self.get_argument('weight', default=None)
        if not _user:
            retjson = generate_ret("express", 302)
        elif not(_sms_txt and _user_name and _user_phone and _dest and _arrival and _locate and _weight):
            retjson = generate_ret("express", 300)
        else:
            try:
                user = self.db.query(Users).filter(Users.phone==_user.phone).one()
                today = datetime.combine(date.today(), time.min) # 当天开始时间
                today_exist = self.db.query(Express).filter(Express.cardnum == user.cardnum,\
                    Express.submittime>today).all()
                if(len(today_exist)>=OneDayMaxCount):
                    retjson = generate_ret("express", 411)
                else:
                    _cur_time = datetime.now()  # 获取当前时间, 将会存入数据库
                    express = Express(
                        cardnum=user.cardnum,
                        sms=_sms_txt,
                        user=_user_name,
                        phone=_user_phone,
                        dest=_dest,
                        arrival=_arrival,
                        locate=_locate,
                        weight=_weight,
                        submittime=_cur_time,
                    )
                    try:
                        self.db.add(express)
                        self.db.commit()
                    except:
                        self.db.rollback()
                        retjson = generate_ret("express", 500)
            except NoResultFound:
                retjson = generate_ret("express", 301)
            except Exception,e:
                retjson = generate_ret("express", 500, str(e))
        self.write_back(retjson)
