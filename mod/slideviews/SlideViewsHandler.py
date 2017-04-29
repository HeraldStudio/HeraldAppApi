#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-27 09:23:51
# @Author  : higuoxing@outlook.com

import tornado.web
import json
from sqlalchemy import desc
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.Basehandler import BaseHandler
from mod.databases.tables import SlideViews

import io
import datetime
from PIL import Image
from qiniu import put_data
from mod.slideviews.SlideViewsConfig import *
from sqlalchemy.orm.exc import NoResultFound

class UploadExceptions(RuntimeError):

    def __init__(self, code, content):
        self.code = code
        self.content = content

class ArgumentExceptions(RuntimeError):

    def __init__(self, code, content):
        self.code = code
        self.content = content

class SlideViewsHandler(BaseHandler):

    def get(self):
        self.write('herald webservice!')

    @gen.coroutine
    def post(self):
        ask_code = self.get_argument('askcode', default = 'unsolved')

        if ask_code == '101':
        #############################################
        #101   Function: Upload a slideview         #
        #      Arguments: title, begintime,         #
        #        endtime, file(in binery)           #
        #############################################
            retjson = {
                'code': 200,
                'content': u'上传成功'
            }
            try:
                title = self.get_argument('title')
                begin_time = self.get_argument('begintime')
                end_time = self.get_argument('endtime')
                file_metas = self.request.files['file']
                if file_metas:
                    for meta in file_metas:
                        fileName = meta['filename']
                        fileType = fileName.split('.')[-1:][0]
                        fileSize = len(meta['body'])
                        begin_time = datetime.datetime.strptime(begin_time,"%Y-%m-%d")
                        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
                        if end_time <= begin_time:
                            raise ArgumentExceptions(401, u'时间参数错误')
                        #Check the image
                        if fileSize > MAX_FILE_SIZE:
                            raise UploadExceptions(401, u'文件过大')
                        if fileType not in ['jpg', 'jpeg', 'png']:
                            raise UploadExceptions(401, '文件格式不符')
                        img = Image.open(io.BytesIO(meta['body']))
                        img_size = img.size
                        if img_size[0] / img_size[1] != PIC_LENGTH / PIC_WIDTH:
                            raise UploadExceptions(401, u'图片尺寸应为1080*432')
                        http_client = AsyncHTTPClient()
                        response = yield http_client.fetch(GET_TOKEN_URL)
                        token = json.loads(response.body)
                        print token
                        #ret, info = put_data(token['token'], token['key'], meta['body'])
                        image_url = token['domain'] + token['key']
                        slideviewsdb = SlideViews(
                            title = title,
                            imageurl = image_url,
                            url = None,
                            begin_time = begin_time,
                            end_time = end_time,
                            key = token['key']
                            )
                        try:
                            self.db.add(slideviewsdb)
                            self.db.commit()
                            self.db.close()
                        except Exception as e:
                            print str(e)
                            retjson['code'] = 402
                            retjson['content'] = u'写入数据库错误'
                else:
                    raise UploadExceptions(400, u'文件不能为空')

            except ArgumentExceptions as e:
                retjson['code'] = e.code
                retjson['content'] = e.content

            except UploadExceptions as e:
                retjson['code'] = e.code
                retjson['content'] = e.content

            except Exception as e:
                print str(e)
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        elif ask_code == '102':
        ################################################
        #102    Function: Delete a slideview           #
        #             Arguments: id                    #
        #       Attention: Please reffer databases     #
        #            before delete any thing           #
        ################################################
            retjson = {
                'code': 200,
                'content': u'删除成功'
            }
            try:
                Id = self.get_argument('id')
                try:
                    matched_image = self.db.query(SlideViews).filter(\
                        SlideViews.id == Id).one()
                    self.db.delete(matched_image)
                    self.db.commit()
                    self.db.close()

                except NoResultFound as e:
                    retjson['code'] = 401
                    retjson['content'] = u'记录不存在'

            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = u'系统错误'

        elif ask_code == '103':
        ############################################
        #103    Function: List slideviews          #
        ############################################
            retjson = {
                'code': 200,
                'content': ''
            }
            try:
                slideViewsList = self.db.query(SlideViews).order_by(SlideViews.begin_time).all()
                ret_data = []
                for item in slideViewsList:
                    tmp = dict(
                        Id          = item.id,
                        title       = item.title,
                        image_url   = item.imageurl,
                        url         = item.url,
                        begin_time  = item.begin_time,
                        end_time    = item.end_time,
                        Key         = item.key,
                        hit_count   = item.hit_count,
                    )
                    ret_data.append(tmp)
                items_per_page = int(self.get_argument('items_per_page', default = len(ret_data)))
                page = int(self.get_argument('page', default = 1))
                total_page = len(ret_data) / items_per_page + len(ret_data) % items_per_page
                if page > total_page - 1 or page < 1:
                    raise ArgumentExceptions(401, u'页码超出范围')
                lower_num = (page - 1) * items_per_page
                larger_num = min((page) * items_per_page, page * items_per_page + \
                   len(ret_data) % items_per_page)
                retjson['content'] = str(ret_data[lower_num:larger_num])
                retjson['max_page'] = total_page - 1

            except ArgumentExceptions as e:
                retjson['code'] = e.code
                retjson['content'] = e.content

            except Exception as e:
                print str(e)
                retjson['code'] = 400
                retjson['content'] = u'系统错误'

        elif ask_code == '104':
        #########################################################
        #104  Function: Synchronize local databases with Qiniu  #
        #                     Arguments: id                     #
        #########################################################
            pass

        self.write(json.dumps(retjson, indent=2, ensure_ascii=False))
        self.finish()

"""
{u'token': u'u5_mJLM8gy6foLG3cWzVJoSquljCX5eSnd9Vc9v1:1NJhFCxSI32-u6n88ktVfD3zARE=:eyJzY29wZSI6ImhlcmFsZC13ZWl4aW46NDZmNjEwYWEzMmUyNDQ5ODg5OTM5MzViZmQ1NTkwYmQiLCJkZWFkbGluZSI6MTQ5MzM5Mjg2M30=', u'domain': u'http://static.myseu.cn/', u'key': u'46f610aa32e244988993935bfd5590bd'}
stat() argument 1 must be encoded string without null bytes, not str
[I 170428 21:21:03 web:1971] 200 POST /herald/api/v1/slideviews (127.0.0.1) 94.27ms
[I 170428 21:21:27 autoreload:204] /Users/eric/Documents/Herald-Studio/HeraldAppApi/mod/slideviews/SlideViewsHandler.py modified; restarting server
{u'token': u'u5_mJLM8gy6foLG3cWzVJoSquljCX5eSnd9Vc9v1:3Qwj8IseJDifyaZVfCFJsfJ7YVs=:eyJzY29wZSI6ImhlcmFsZC13ZWl4aW46MzE4ZTllYTNmMzJiNDUxNjhkNjYwY2E2MDliMmZmZGUiLCJkZWFkbGluZSI6MTQ5MzM5Mjg5MX0=', u'domain': u'http://static.myseu.cn/', u'key': u'318e9ea3f32b45168d660ca609b2ffde'}
exception:None, status_code:200, _ResponseInfo__response:<Response [200]>, text_body:{"hash":"FutYHfRL85bwvuG_hG7l_lRPbOYL","key":"318e9ea3f32b45168d660ca609b2ffde"}, req_id:LHgAADWAo8RfkrkU, x_log:body:20;TBLMGR:1;RS:2;CFGG:8;s.ph;s.put.tw;s.put.tr:2;s.put.tw;s.put.tr:3;s.ph;PFDS:3;PFDS:7;rs33_7.sel/not found;rdb.g/no such key;DBD/404;v4.get:1/Document not found;rs33_7.ups;rwro.ups:2;mc.s;RS:3;rs.put:11;rs-upload.putFile:20;UP:76
"""
