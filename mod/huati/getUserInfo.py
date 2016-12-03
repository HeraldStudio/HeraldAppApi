# coding=utf-8
'''
 @author：黄鑫晨
 2016.12
'''

import json
import urllib
import urllib2


_uuid = 'fd4b2c58db1e394d312c9e7ca53e588999f491ce'
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

if __name__ == "__main__":
    print get_card(_uuid)
