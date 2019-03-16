"""__author__ = 干友恒"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# 生成数据库访问对象db
db = SQLAlchemy()


class User(db.Model):
    """用户的类"""
    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 定义不能为空且唯一的用户账号
    username = db.Column(db.String(11), unique=True, nullable=False)
    # 定义不能为空的密码
    password = db.Column(db.String(255), nullable=False)
    # 记录用户是否被删除
    is_delete = db.Column(db.Boolean, default=0)
    # 用户创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 定义创建在数据库中的表名
    __tablename__ = 'user'

    def save(self):
        """数据保存"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ArticleType(db.Model):
    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    art_name = db.Column(db.String(10), nullable=False)

    arts = db.relationship('Article', backref='tp')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __tablename__ = 'art_type'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(30), nullable=False)

    desc = db.Column(db.String(120))

    content = db.Column(db.Text, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now)

    type_id = db.Column(db.Integer, db.ForeignKey('art_type.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserInform(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(11), unique=True, nullable=False)

    sex = db.Column(db.Boolean, nullable=False, default=0)

    birth = db.Column(db.String(11))

    tel = db.Column(db.String(11))

    email = db.Column(db.String(20))

    city = db.Column(db.String(11))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()




