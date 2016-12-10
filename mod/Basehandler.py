# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.web
from databases.tables import Access_Token,Users,ExpressAdmin
import json

class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        """允许提交跨域请求
        """
        self.set_header("Access-Control-Allow-Origin", "*")

    def options(self):
        retjson = {'code':200}
        self.write_back(retjson)
        
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
