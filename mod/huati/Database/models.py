# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# DB_CONNECT_STRING = 'mysql+mysqldb://root:hxc@127.0.0.1/hearld_activity?charset=utf8'
# DB_CONNECT_STRING = 'mysql+mysqldb://root:hxc@127.0.0.1:3306/hearld_activity?charset=utf8'
DB_CONNECT_STRING = 'mysql+mysqldb://root:@127.0.0.1/hearld_activities?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)  # 返回数据库引擎，即连接数据库
connection = engine.connect()

Base = declarative_base()  # declarative_base() 创建了一个 BaseModel 类，这个类的子类可以自动与一个表关联。
# Construct a base class for declarative class definitions.

if(engine!=None):
    print "数据库连接成功，return"
    print connection
else:
    print "未找到数据库"


