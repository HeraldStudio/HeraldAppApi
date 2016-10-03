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
from mod.huati.TopicHandler import TopicHandler
from mod.yuyue.yuyueHandler import YuyueHandler
from mod.databases.db import engine

from mod.huodong.getHuodong import getHuodong
from mod.huodong.HuodongCommit import HuodongCommit
from mod.huodong.HuodongLogin import HuodongLogin
from mod.huodong.upload import UploadPichandler

from mod.kuaidi.deleteRecord import DeleteRecordHandler
from mod.kuaidi.getTimeList import GetTimeListHandler
from mod.kuaidi.modifyState import ModifyStateHandler
from mod.kuaidi.queryAll import QueryHandler
from mod.kuaidi.queryByCardnum import QueryByCardnumHandler
from mod.kuaidi.submit import SubmitHandler
from mod.kuaidi.adminLogin import ExpressAdminLoginHandler
from mod.emptyroom.handler import NewGetHandler
from mod.emptyroom.oldHandler import GetHandler,SimpleHander,ComplexHander
from mod.service.feedbackHandler import FeedBackHandler,FeedBackSuccessHandler,FeedBackDetailsHandler

from config import COOKIE_SECRET

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
            (r'/herald/api/v1/deliver/delete', DeleteRecordHandler),
            (r'/herald/api/v1/deliver/timelist', GetTimeListHandler),
            (r'/herald/api/v1/deliver/change', ModifyStateHandler),
            (r'/herald/api/v1/deliver/submit', SubmitHandler),
            (r'/herald/api/v1/deliver/admin_query', QueryHandler),
            (r'/herald/api/v1/deliver/query', QueryByCardnumHandler),
            (r'/herald/api/v1/deliver/admin_login', ExpressAdminLoginHandler),
            (r'/herald/api/v1/deliver/admin_login', ExpressAdminLoginHandler),
            (r"/herald/api/v1/queryEmptyClassrooms/m", NewGetHandler),
            (r"/herald/api/v1/queryEmptyClassrooms/m/(.*)", NewGetHandler),
            (r"/herald/api/v1/queryEmptyClassrooms/simple", SimpleHander),
            (r"/herald/api/v1/queryEmptyClassrooms/complex", ComplexHander),
            (r"/herald/api/v1/feedback",FeedBackHandler),
            (r"/herald/api/v1/feedback/success", FeedBackSuccessHandler),
            (r"/herald/api/v1/feedback/details", FeedBackDetailsHandler),
            (r'/herald/api/v1/topic', TopicHandler),
            (r'/herald/.*', PageNotFoundHandler)


            ]
        settings = dict(
            cookie_secret=COOKIE_SECRET,
            template_path= os.path.join(os.path.dirname(__file__), 'templates'),
            static_path= os.path.join(os.path.dirname(__file__), 'static'),
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
