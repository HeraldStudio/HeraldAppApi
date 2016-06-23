# -*- coding: utf-8 -*-
#!/usr/bin/env python

# @Date    : 2016-05-13 11:20:05
# @Author  : jerry.liangj@qq.com

import json
import datetime
from tornado import websocket
from ..databases.tables import Biaobai,DenyIp

class biaobaiHandler(websocket.WebSocketHandler):
    clients = set()
    admin_ip = []
    deny_ip = []

    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    @staticmethod
    def send_to_all(message):
      for c in biaobaiHandler.clients:
          c.write_message(json.dumps(message))

    def open(self):
        # print self,"open"
        biaobaiHandler.clients.add(self)
        ret = {
            'type':'info',
            'number':len(biaobaiHandler.clients)
        }
        biaobaiHandler.send_to_all(ret)
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = self.db.query(Biaobai).filter(Biaobai.posttime<datetime.datetime.now())\
            .order_by(Biaobai.posttime.desc()).limit(20)
            ret = {'type':'open','content':[]}
            for message in result:
                ret['content'].append({
                    'type':'user',
                    'name':message.user,
                    'message':message.content,
                    'time':message.posttime.strftime("%Y-%m-%d %H:%M:%S"),
            })
            self.write_message(ret)
        except Exception,e:
            print str(e)
            # print str(e)
        # self.write_message(json.dumps(ret))
        # self.stream.set_nodelay(True)
    def admin_message(self,message):
        ret = {
            'type':'admin',
            'message':message,
            'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        biaobaiHandler.send_to_all(ret)
    def on_message(self, message):
        try:
            message = json.loads(message)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remote_ip = self.request.remote_ip
            if remote_ip in biaobaiHandler.admin_ip:
                self.admin_message(message['content'])
            if remote_ip in biaobaiHandler.deny_ip:
                self.admin_message(u"您已被禁言")
            else:
                ret = {
                    'type':'user',
                    'name':message['user'],
                    'message':message['content'],
                    'time':now,
                }
                biaobaiHandler.send_to_all(ret)
            
                message = Biaobai(user=message['user'],ip=remote_ip,content = message['content'],posttime=now)
                self.db.add(message)
                self.db.commit()
                result = self.db.query(DenyIp).all()
                biaobaiHandler.deny_ip = []
                for i in result:
                    biaobaiHandler.deny_ip.append(i.ip)
        except Exception,e:
            pass
            # print str(e)

        # self.close()

    def on_close(self):
        # print self,"closed"
        biaobaiHandler.clients.remove(self)
        ret = {
            'type':'info',
            'number':len(biaobaiHandler.clients)
        }
        biaobaiHandler.send_to_all(ret)