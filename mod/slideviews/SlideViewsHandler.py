#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-27 09:23:51
# @Author  : higuoxing@outlook.com

import tornado.web
import json
from sqlalchemy import or_
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from mod.Basehandler import ManagerHandler
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


class SlideViewsHandler(ManagerHandler):

    def get(self):
        self.write('herald webservice!')

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):

        retjson = {
            'code': 400,
            'content': u'系统错误'
        }
        
        askcode = self.get_argument('askcode', default = 'unsolved')

        if askcode == '101':
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

        elif askcode == '102':
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

        
        elif askcode == '103':
            
            try:
                Id = self.get_argument('id')
            except Exception as e:

                retjson = {
                    'code' : 400,
                    'content' : u'缺少参数'
                }

            try:
                self.db.query(SlideViews).filter( \
                    SlideViews.id == Id).one()
                matched_slide_view = self.db.query(SlideViews).filter( \
                    SlideViews.id == Id).scalar()
                title = self.get_argument('title', default = None)
                imageurl = self.get_argument('imageurl', default = None)
                url = self.get_argument('url', default = None)
                begintime = self.get_argument('begintime', default = None)
                endtime = self.get_argument('endtime', default = None)
                if title:
                    matched_slide_view.title = title
                if imageurl:
                    matched_slide_view.imageurl = imageurl
                if url:
                    matched_slide_view.url = url
                if begintime:
                    matched_slide_view.begintime = begintime
                if endtime:
                    matched_slide_view.endtime = endtime
                retjson['code'] = 200
                retjson['content'] = u'修改成功'
                self.db.commit()
                self.db.close()

            except NoResultFound as e:
                retjson['code'] = 400
                retjson['content'] = u'记录不存在'

            except Exception as e:
                retjson['code'] = 400
                retjson['content'] = u'系统错误'

        elif askcode == '104':
        ############################################
        #104    Function: List slideviews          #
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
                total_page = len(ret_data) / items_per_page + 1
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
                #print str(e)
                retjson['code'] = 400
                retjson['content'] = u'系统错误'

        elif askcode == '105':
            
            retjson = {
                'code': 200,
                'content': ''
            }

            ret_data = []
            try:
                pattern = self.get_argument('pattern')
                matchedSlideViews = self.db.query(SlideViews).filter( \
                    SlideViews.title.like(pattern + '%')).all()
                for item in matchedSlideViews:
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
                retjson['content'] = str(ret_data)

            except Exception as e:
                print str(e)
                retjson['code'] = 400
                retjson['content'] = u'系统错误'

        self.write(json.dumps(retjson, indent=2, ensure_ascii=False))
        self.finish()
