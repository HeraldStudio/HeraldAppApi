#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-03 20:03:27
# @Author  : Higuoxing@outlook.com

import tornado.web
import json
from sqlalchemy import desc
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from sqlalchemy.orm.exc import NoResultFound
from mod.Basehandler import BaseHandler
from mod.databases.tables import PushMessage

class ArgumentExceptions(RuntimeError):

	def __init__(self, code, content):
		
		self.code = code
		self.content = content

class PushMessageHandler(BaseHandler):

	def get(self):

		self.write('Herald webservice!')

	def post(self):

		retjson = {
			'code': 400,
			'content': u'系统错误'
		}
		askcode = self.get_argument('askcode')

		if askcode == '101':
			try:
				content = self.get_argument('content', default = None)
				url = self.get_argument('url', default = None)
				priority = self.get_argument('priority', default = 1)
				schoolnum = self.get_argument('schoolnum', default = None)
				versiontype = self.get_argument('versiontype', default = None)
				if schoolnum or versiontype:
					pushMessagedb = PushMessage(
							content = content,
							url = url,
							priority = priority,
							schoolnum = schoolnum,
							versiontype = versiontype
							)
					retjson = {
						'code': 200,
						'content': u'推送成功'
					}
					try:
						self.db.add(pushMessagedb)
						self.db.commit()
						self.db.close()
					except Exception as e:
						retjson['code'] = 400
						retjson['content'] = u'写入数据库失败'

				else:
					raise ArgumentExceptions(400, u'参数错误')

			except ArgumentExceptions as e:
				retjson['code'] = e.code
				retjson['content'] = e.content

			except Exception as e:
				retjson['code'] = 500
				retjson['content'] = u'系统错误'

		elif askcode == '102':
			
			retjson = {
				'code': 400,
				'content': u'系统错误'
			}

			try:
				Id = self.get_argument('id')
				
				try:
					matched_message = self.db.query(PushMessage).filter(\
						PushMessage.id == Id).one()
					self.db.delete(matched_message)
					self.db.commit()
					self.db.close()
					retjson['code'] = 200
					retjson['content'] = u'删除成功'

				except NoResultFound as e:
					retjson['code'] = 401
					retjson['content'] = u'记录不存在'
			
			except Exception as e:
				retjson['code'] = 400
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
				self.db.query(PushMessage).filter( \
					PushMessage.id == Id).one()
				matched_message = self.db.query(PushMessage).filter( \
					PushMessage.id == Id).scalar()
				content = self.get_argument('content', default = None)
				url = self.get_argument('url', default = None)
				priority = self.get_argument('priority', default = None)
				schoolnum = self.get_argument('schoolnum', default = None)
				versiontype = self.get_argument('versiontype', default = None)
				if content:
					matched_message.content = content
				if url:
					matched_message.url = url
				if priority:
					matched_message.priority = priority
				if schoolnum:
					matched_message.schoolnum = schoolnum
				if versiontype:
					matched_message.versiontype = versiontype
				retjson['code'] = 200
				retjson['content'] = u'修改成功'
				self.db.commit()
				self.db.close()

			except NoResultFound as e:
				retjson['code'] = 400
				retjson['content'] = u'记录不存在'

			except Exception as e:
				pass

		elif askcode == '104':
			retjson = {
				'code': 200,
				'content': ''
			}

			try:
				pushMessageList = self.db.query(PushMessage).order_by(PushMessage.id).all()
				ret_data = []
				for item in pushMessageList:
					tmp = dict(
						Id          = item.id,
						content     = item.content,
						url         = item.url,
						schoolnum   = item.schoolnum,
						versiontype = item.versiontype,
						priority    = item.priority,
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
			pass

		self.write(json.dumps(retjson, indent=2, ensure_ascii=False))
		self.finish()

