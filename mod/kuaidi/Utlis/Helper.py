# -*- coding=utf-8 -*-
"""
Created on Aug 10, 2016

@author: corvo
"""

import json
import urllib
import urllib2


def get_card(_uuid):
    """ 通过uuid 获取一卡通号 """
    _check_path = 'http://www.heraldstudio.com/api/user'

    #     print (_uuid)
    params = {'uuid': _uuid}

    data = urllib.urlencode(params)
    req = urllib2.Request(_check_path, data)
    response = urllib2.urlopen(req)

    res_json = response.read()
    encodejson = json.loads(res_json)

    return encodejson['content']['cardnum']


def check_superuser(_superuser):
    """ 修改状态时, 用于超级用户是否有效 """

    return True
