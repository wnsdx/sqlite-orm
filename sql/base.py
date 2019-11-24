#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from sqlalchemy import *

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# 创建映射
Base = declarative_base()

# 定义映射类User,继承上一步创建的Base
class User(Base):
    # 指定本类映射到的users表
    __tablename__ = 'users'

    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

if __name__=='__main__':
    # 查看映射对应的表
    User.__table__

    # check_same_thread = False - ---sqlite默认建立的对象只能让建立该对象的线程使用，
    # 而sqlalchemy是多线程的所以我们需要指定check_same_thread = False来让建立的对象任
    # 意线程都可使用
    engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=True)

    # 创建数据表
    Base.metadata.create_all(engine)
    # 建立会话
    Session = sessionmaker(bind=engine)
    # 创建Session类实例
    session = Session()

    # 创建User类实例
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')

    # 将该实例插入到users表
    session.add(ed_user)

    # 一次插入多条记录形式
    session.add_all(
        [User(name='wendy', fullname='Wendy Williams', password='foobar'),
         User(name='mary', fullname='Mary Contrary', password='xxg527'),
         User(name='fred', fullname='Fred Flinstone', password='blah')]
    )

    # 当前更改只是在session中，需要使用commit确认更改才会写入数据库
    session.commit()

    # 指定User类查询users表，查找name为'ed'的第一条数据
    our_user = session.query(User).filter_by(name='ed').first()
    print("[ret] our_user is ed_user?:", our_user is ed_user)
    print("[ret]", our_user.name)
    print("[ret]", our_user.fullname)
    print("[ret]", our_user.password)

    table_and_column_name = User
    filter = (User.name == 'ed')

    our_user = session.query(table_and_column_name).filter(filter).first()

    print("[ret] our_user is ed_user?:", our_user is ed_user)
    print("[ret]", our_user.name)
    print("[ret]", our_user.fullname)
    print("[ret]", our_user.password)
    # our_user
    #
    # # 比较ed_user与查询到的our_user是否为同一条记录
    # ed_user is our_user

    # 要修改需要先将记录查出来
    mod_user = session.query(User).filter_by(name='ed').first()

    # 将ed用户的密码修改为modify_paswd
    mod_user.password = 'modify_passwd'

    # 确认修改
    session.commit()

    pass

    # 要删除需要先将记录查出来
    del_user = session.query(User).filter_by(name='ed').first()

    # 打印一下，确认未删除前记录存在
    del_user

    # 将ed用户记录删除
    session.delete(del_user)

    # 确认删除
    session.commit()

    # 遍历查看，已无ed用户记录
    for user in session.query(User):
        print(user)

