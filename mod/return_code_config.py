# -*- coding: utf-8 -*-
#!/usr/bin/env python


#所有返回的code对应的content
codeTable = {
    300:u'参数太少',
    301:u'用户不存在',
    302:u'请先登录',
    400:u'密码错误',
    401:u'密码太短',
    402:u'手机号格式不正确',
    403:u'该手机号已被注册',
    404:u'验证码格式不正确',
    405:u'验证码已过期',
    406:u'验证码不正确',
    407:u'已达每日最大发送次数',
    408:u'发送间隔小于两分钟',
    409:u'参数格式错误',
    410:u'操作权限不足',
    411:u'输入简介过长',
    412:u'非法操作',

    500:u'系统错误'
}

Express_CodeTable = {
    200: u'操作成功',
    300: u'参数太少',
    301: u'用户不存在',
    302: u'请先登录',
    303: u'参数错误',
    304: u'快件已有人接单',
    305: u'用户错误',
    400: u'密码错误',
    401: u'密码太短',
    402: u'手机号格式不正确',
    403: u'该手机号已被注册',
    404: u'验证码格式不正确',
    405: u'验证码已过期',
    406: u'验证码不正确',
    407: u'已达每日最大发送次数',
    408: u'发送间隔小于两分钟',
    409: u'参数格式错误',
    410: u'订单不存在',
    411: u'超过当日最大下单数',

    500: u'系统错误'
}

def generate_ret(table,code,content=None):
    key_to_Table = {
        'express': Express_CodeTable
    }
    retjson = {}
    try:
        retjson['code'] = code
        if content:
            retjson['content'] = content
        else:
            retjson['content'] = key_to_Table[table][code]
        return retjson
    except Exception,e:
        return {'code':500,'content':u'系统错误'}
