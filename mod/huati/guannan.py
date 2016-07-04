#
# Skip to content
# This repository
#
#     Pull requests
#     Issues
#     Gist
#
#     @half-programmer
#
# Please verify your email address to access all of GitHub's features.
# An email containing verification instructions was sent to Kingxc96@outlool.com.
#
# 6
# 0
#
#     1
#
# liang-jie/FitGo
# Code
# Issues 0
# Pull requests 0
# Wiki
# Pulse
# Graphs
# FitGo/mod/auth/Password_Handler.py
# ec67c6a on 17 Sep 2015
# yue-b 删除print
# @liang-jie
# @qinshimeng18
# 78 lines (74 sloc) 2.55 KB
# # -*- coding: utf-8 -*-
# #!/usr/bin/env python
# import tornado.web
# import tornado.gen
# from Base_Handler import BaseHandler
# from ..databases.tables import UsersCache,CookieCache
# from sqlalchemy.orm.exc import NoResultFound
# import json
# from time import time
# import uuid
# import re
# import hashlib,random,string
#
# class PasswordHandler(BaseHandler):
# 	# @tornado.web.authenticated
# 	def put(self):
# 		old_passwd = self.get_argument('old_password')
# 		new_passwd = self.get_argument('new_password')
# 		user_cookie = self.current_user
# 		# user_cookie = self.get_argument('uid')
# 		retjson = {"code":200,"content":""}
# 		try:
# 			usr1=self.db.query(UsersCache).filter(UsersCache.uid==user_cookie.uid).one()
# 			old_salt = usr1.salt
# 			old_password = hashlib.md5(old_salt.join(old_passwd)).hexdigest()
# 			if old_password == usr1.password:
# 				new_salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
# 				usr1.password = hashlib.md5(new_salt.join(new_passwd)).hexdigest()
# 				usr1.salt = new_salt
# 				self.db.add(usr1)
# 				try:
# 					self.db.commit()
# 				except Exception,e:
# 					self.db.rollback()
# 					retjson['code'] = 400
# 					retjson['content'] = 'store data wrong!Try again'
# 				retjson['content'] = "passwd update ok!"
# 			else:
# 				retjson['code'] = 400
# 				retjson['content'] = 'old password is wrong'
#
# 		except NoResultFound:
# 			retjson['code'] = 400
# 			retjson['content'] = 'Please check your old password'
# 		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
# 		self.write(ret)
# 	def post(self):
# 		try:
# 			arg_info_email = self.get_argument('info_email')
# 			arg_student_card = self.get_argument('student_card')
# 			arg_new_password = self.get_argument('new_password')
# 			salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
# 			arg_new_password = hashlib.md5(salt.join(arg_new_password)).hexdigest()
# 			retjson = {"code":200,"content":""}
# 			try:
# 				user = self.db.query(UsersCache).filter(UsersCache.info_email==arg_info_email,\
# 					UsersCache.student_card==arg_student_card).one()
# 				if user:
# 					user.password = arg_new_password
# 					user.salt = salt
# 					self.db.add(user)
# 					retjson['content'] = "passwd update ok!"
# 				else:
# 					retjson = {'code':400,'content':'no user'}
# 				try:
# 					self.db.commit()
# 				except Exception,e:
# 					self.db.rollback()
# 					retjson['code'] = 400
# 					retjson['content'] = 'store data wrong!Try again'
# 			except Exception,e:
# 				retjson = {'code':400,'content':'failed to query database'}
# 		except Exception,e:
# 			retjson = {'code':400,'content':'no parameters'}
# 		ret = json.dumps(retjson,ensure_ascii=False, indent=2)
# 		self.write(ret)
#
#
#     Status API Training Shop Blog About
#
#     © 2016 GitHub, Inc. Terms Privacy Security Contact Help
#
