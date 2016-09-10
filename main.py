# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os,json
from tornado.options import define, options

from sqlalchemy.orm import scoped_session, sessionmaker
from mod.auth.login import LoginHandler
from mod.auth.registerHandler import RegisterHandler
from mod.yuyue.yuyueHandler import YuyueHandler
from mod.databases.db import engine
from mod.huodong.getHuodong import getHuodong
from mod.huodong.HuodongCommit import HuodongCommit
from mod.huodong.HuodongLogin import HuodongLogin
from mod.huodong.upload import UploadPichandler

define("port", default=7000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/herald/api/v1/auth/login',LoginHandler),
            (r'/herald/api/v1/auth/reg',RegisterHandler),
            (r'/herald/api/v1/yuyue',YuyueHandler),
            (r'/herald/api/v1/huodong/get',getHuodong),
            (r'/herald/api/v1/huodong/commit',HuodongCommit),
            (r'/herald/api/v1/huodong/login',HuodongLogin),
            (r'/herald/api/v1/huodong/upload',UploadPichandler),
            (r'/herald/.*', PageNotFoundHandler)
            ]
        settings = dict(
            cookie_secret="8DB90KLP8371B5AEAC5E64C6042415EF",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
            # autoload=True,
            # autoescape=None
        )
        tornado.web.Application.__init__(self, handlers,**settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('404.html')
    def post(self):
        self.render('404.html')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    Application().listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
