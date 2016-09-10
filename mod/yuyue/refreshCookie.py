# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2015-11-18 21:20:05
# @Author  : jerry.liangj@qq.com
import time,json
import urllib
from tornado.httpclient import HTTPRequest, HTTPClient
from ..databases.tables import Users
from sqlalchemy.orm.exc import NoResultFound

TIME_OUT = 8000
LOGIN_URL = 'https://mobile4.seu.edu.cn/_ids_mobile/login18_9'

def refreshCookie(db,token):
    if int(token.last_time)+TIME_OUT<int(time.time()):
        try:
            user = db.query(Users).filter(Users.phone == token.phone).one()
            state,response = getCookie(user.cardnum,user.card_password)
            if state:
                # print 'state ok'+response
                token.cookie = response
                token.last_time = int(time.time())
                db.add(token)
                db.commit()
                return True,response
            else:
                # print 'state false'
                return False,None
        except NoResultFound:
            return False,u'该用户不存在'
        except Exception,e:
            db.db.rollback()
            return False,str(e)
    else:
        # print 'exist'
        return True,token.cookie

def getCookie(cardnum,card_pwd):
    # print "refresh"
    data = {
            'username':cardnum,
            'password':card_pwd
        }
    try:
        client = HTTPClient()
        request = HTTPRequest(
            LOGIN_URL,
            method='POST',
            body=urllib.urlencode(data),
            validate_cert=False,
            request_timeout=4)
        response = client.fetch(request)
        header = response.headers
        if 'Ssocookie' in header.keys():
            headertemp = json.loads(header['Ssocookie'])
            cookie = headertemp[0]['cookieName']+"="+headertemp[0]['cookieValue']
            cookie += ";"+header['Set-Cookie'].split(";")[0]
            return True,cookie
        else:
            return False,"No cookie"
    except Exception,e:
        # print str(e)
        return False,str(e)