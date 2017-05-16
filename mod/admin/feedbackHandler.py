#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
import json
from math import ceil
from mod.Basehandler import ManagerHandler
from mod.databases.feedback import FeedBack
from sqlalchemy.orm.exc import NoResultFound

class ArgumentExceptions(RuntimeError):
    def __init__(self,code,content):
        self.code=code
        self.content=content

class FeedbackHandler(ManagerHandler):

    @tornado.web.authenticated
    def post(self):
        ask_code=self.get_argument('askcode',None)
        ret={
            'content':u'请求码错误',
            'code':201
        }

        if ask_code=='101':
            offset=int(self.get_argument('page',1))-1
            limit=float(self.get_argument('items_per_page',20))

            try:
                if offset<0 or limit<=0:
                    raise ArgumentExceptions(202,u'请求参数错误')
                ret['max_page'] = int(ceil(self.db.query(FeedBack).count() / limit))
                if offset>ret['max_page']-1:
                    raise ArgumentExceptions(203,u'页数超出范围')
                FB=self.db.query(FeedBack).group_by(FeedBack.date.desc()).limit(limit).offset(offset*limit).all()
                data=[]
                for fb in FB:
                    tmp=dict(
                        id   =fb.id,
                        text = fb.text,
                        date = str(fb.date),
                        user = fb.user,
                        response = fb.response,
                        state = fb.state
                    )
                    data.append(tmp)
                ret['content']=data

            except ArgumentExceptions as e:
                ret['content']=e.content
                ret['code']=e.code
            except NoResultFound:
                ret['content']=u'未找到数据'
                ret['code']=204
            except Exception:
                ret['content']=u'数据库查询出错'
                ret['code']=205
        self.write(json.dumps(ret, indent=2, ensure_ascii=False))

    def get(self):
        self.write('herald webservice!')
