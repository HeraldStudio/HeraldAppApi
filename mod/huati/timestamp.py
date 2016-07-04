# -*- coding: utf-8 -*-
import time, datetime


def timestamp_datetime(value):  # 时间戳转换为时间字符串
 format = '%Y-%m-%d %H:%M:%S'
 # value为传入的值为时间戳(整形)，如：1332888820
 value = time.localtime(value)
 ## 经过localtime转换后变成
 ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
 # 最后再经过strftime函数转换为正常日期格式。
 dt = time.strftime(format, value)
 time.mktime(time.strptime('YYYY-MM-DD HH:MM:SS', '%Y-%m-%d %H:%M:%S'))
 return dt



def datetime_timestamp(dt):  # 字符串转换为时间戳
  #dt为字符串
  #中间过程，一般都需要将字符串转化为时间数组
    #sdt=time.strptime(dt, '%Y-%m-%d %H:%M:%S')   # 把一个字符串转换成时间元组
  ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
  #将"2012-03-28 06:53:40"转化为时间戳
 # s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
#  return int(s)
    s = dt.lstrip('(').rstrip(')')  # 截掉左右字符
    d = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S") #格式符参考下表
    return time.mktime(d.timetuple())

def getlocaltime():
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime()
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt