#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-27 09:23:51
# @Author  : higuoxing@outlook.com

import tornado.web
import json
from sqlalchemy import desc
from mod.Basehandler import BaseHandler
from mod.databases.tables import Circular
from mod.circular.CircularFunctions import CircularFunctions

class CircularHandler(Basehandler):

	def get(self):
		self.write("herald web service")

	def post(self):
		ask_code = self.get_argument('askcode', default = 'unsolved')
		retjson = {
			"content" = "none",
			"code" = 200
		}

		if ask_code == '101':
			"""
			upload
			"""
			pass

		elif ask_code == '102':
			"""
			delete
			"""
			pass

		elif ask_code == '103':
			"""
			search
			"""
			pass

		self.write(json.dumps(retjson, indent=2, ensure_ascii=False))

