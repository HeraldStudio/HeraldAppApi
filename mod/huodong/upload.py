# -*- coding: utf-8 -*-

__author__ = 'LiangJ'

import tornado.web
import hashlib
import json,io
from ..Basehandler import BaseHandler
from ..databases.tables import ActivCommitUser,Activity
from sqlalchemy.orm.exc import NoResultFound
from PIL import Image
import traceback

class UploadException(RuntimeError):
    def __init__(self,code,content):
        self.code = code
        self.content = content

MAX_FILE_SIZE = 500*1024

class UploadPichandler(BaseHandler):

    def post(self):
        upload_path = 'http://www.heraldstudio.com/herald/static/img'
        save_path = 'static/img'
        retjson = {'code':200,'content':'success'}
        try:
            request_cookie = self.get_secure_cookie('ActivityCommitter')
            if request_cookie:
                matched_user = self.db.query(ActivCommitUser).filter(ActivCommitUser.cookie == request_cookie).one()
                file_metas = self.request.files['file']
                if file_metas:
                    for meta in file_metas:
                        filename = meta['filename']
                        houzhui = filename.split('.')[-1:][0]
                        file_size = len(meta['body'])
                        if file_size>MAX_FILE_SIZE:
                            raise UploadException(401,u'文件过大')
                        if houzhui not in ['jpg','png']:
                            raise UploadException(401,u'文件格式不支持')
                        img = Image.open(io.BytesIO(meta['body']))
                        pic_size = img.size
                        if float(pic_size[0])/pic_size[1] != 2.5:
                            raise UploadException(401,u'图片比例不是5:2')
                        img = img.resize((500,200))
                        shaobj = hashlib.md5()
                        shaobj.update(meta['body'])
                        filehash = shaobj.hexdigest()
                        filepath = save_path+'/'+filehash+'.jpg'
                        database_path = upload_path+'/'+filehash+'.jpg'
                        img.save(filepath,'jpeg')
                        retjson['content'] = database_path
                else:
                    picurl = self.get_argument('pic_url')
                    if picurl:
                        retjson['content'] = picurl
                    else:
                        retjson['code'] = 500
                        retjson['content'] = u'文件为空'
            else:
                raise UploadException(400,u'请先登录')
        except UploadException,e:
            retjson['code'] = e.code
            retjson['content'] = e.content
        except NoResultFound:
            retjson['code'] = 400
            retjson['content'] = u'请先登录'
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = u'系统错误'
        self.write(json.dumps(retjson,ensure_ascii=False, indent=2))


