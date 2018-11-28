# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# 数据库配置
class Config(object):
    #设置连接数据库的URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/flask_python'

    # 自动跟踪数据库
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config.from_object(Config)

# 创建SQLAlchemy数据库交互对象
db = SQLAlchemy(app)


class Role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "tbl_roles" # 表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    user = db.relationship("User", backref="role")


class User(db.Model):
    """用户表"""
    __tablename__ = "tbl_users" # 表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))




if __name__ == "__main__":
    # 清除数据库里的所有数据
    db.drop_all()

    # 创建所有的表
    db.create_all()

    # 添加记录
    role1 = Role(name="admin") # 创建对象
    db.session.add(role1) # session记录对象任务
    db.session.commit() # 提交任务到数据库中

    role2 = Role(name="stuff")
    db.session.add(role2)
    db.session.commit()

    us1 = User(name='wang',email='wang@163.com', password='123456',role_id=role1.id)
    us2 = User(name='zhang',email='zhang@189.com', password='201512',role_id=role2.id)
    us3 = User(name='chen',email='chen@126.com', password='987654',role_id=role2.id)
    us4 = User(name='zhou',email='zhou@163.com', password='456789',role_id=role1.id)

    db.session.add_all([us1,us2,us3,us4]) # 一次添加多条数据
    db.session.commit()