# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
import tornado.gen
from databases.tables import Access_Token,Users,ExpressAdmin
from sqlalchemy.orm.exc import NoResultFound
import json

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    def get_current_user(self):
        # token = self.get_argument("token",None)
        token = self.request.headers['Token'] if 'Token' in self.request.headers.keys() else None
        if token:
            try:
                token = self.db.query(Access_Token).filter(Access_Token.token==token).one()
                return token
            except:
                return False
        else:
            return False
    def get_express_admin(self):
        token = self.request.headers['Expressadmin'] if 'Expressadmin' in self.request.headers.keys() else None
        if token:
            try:
                token = self.db.query(ExpressAdmin).filter(ExpressAdmin.token==token).one()
                return token
            except:
                return False
        else:
            return False

    def write_back(self,content):
        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header('Access-Control-Allow-Methods','GET,POST')
        self.set_header('Access-Control-Allow-Headers','token,Expressadmin')
        self.write(json.dumps(content,ensure_ascii=False, indent=2))
        self.finish()