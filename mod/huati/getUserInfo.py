# coding=utf-8
'''
 @author：黄鑫晨
 2016.12
'''

import json
import urllib
import urllib2

from ..Basehandler import BaseHandler
from ..databases.tables import Users
_uuid = 'fd4b2c58db1e394d312c9e7ca53e588999f491ce'


def get_name_from_uuid(_uuid):
    """ 通过uuid 获取一卡通号，获得真实姓名 """
    _check_path = 'http://www.heraldstudio.com/api/user'

    #     print (_uuid)
    params = {'uuid': _uuid}

    data = urllib.urlencode(params)
    req = urllib2.Request(_check_path, data)
    response = urllib2.urlopen(req)

    res_json = response.read()
    encodejson = json.loads(res_json, encoding="utf-8")

    return encodejson['content']['name']


class User_info_handler(object):
    def __init__(self, db):
        self.db = db
    '''
    完善用户信息，将用户真实姓名写入user表中
    '''
    def complete_user_name(self, cardnum, uuid):
        '''
            从一卡通获取用户真实姓名，如果原来是空则增加到数据库中
            :return:
            '''
        try:
            user = self.db.query(Users).filter(Users.cardnum == cardnum).one()
            # 已存则返回真实姓名
            if user.name:
                pass
            # 没存则获取并存再返回
            else:
                # 返回真实姓名
                real_name = get_name_from_uuid(uuid)
                # 将真实姓名存入到数据库中
                user.name = real_name
                try:
                    self.db.commit()
                except Exception, e:
                    print e
        except Exception, e:
            print e

    def get_user_name_from_cardnum(self, cardnum):
        '''
        从一卡通获取用户真实姓名
        :return:
        '''

        try:
            user = self.db.query(Users).filter(Users.cardnum == cardnum).one()
            # 已存则返回真实姓名
            if user.name:
                return user.name
        except Exception, e:
             print e

    # 匿名评论模型
    def get_comment_model(self, each, is_parased, ano):
        '''

        :param each: 传入评论的一项
        :param is_parased: 是否点过赞
        :param ano: 是否匿名,1为匿名
        :return:
        '''
        if ano == 1:
            # 匿名
            comment_anonymous = dict(
                time=each.commentT.strftime('%Y-%m-%d %H:%M:%S'),
                cardnum='匿名用户'.decode('utf-8'),
                likeN=each.likeN,
                content=each.content,
                cid=each.id,
                parase=is_parased  # 是否点过赞
            )
            return comment_anonymous
        elif ano == 0:
            # 实名评论
            comment_real = dict(
                time=each.commentT.strftime('%Y-%m-%d %H:%M:%S'),
                cardnum='匿名用户'.decode('utf-8'),
                likeN=each.likeN,
                content=each.content,
                cid=each.id,
                parase=is_parased  # 是否点过赞
            )
            return comment_real


def check_superuser(_superuser):
    """ 修改状态时, 用于超级用户是否有效 """

    return True

if __name__ == "__main__":
    print get_card(_uuid)
