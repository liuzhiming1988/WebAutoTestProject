# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class DbInfo(db.Model):
    __tablename__ = 'db_info'

    id = db.Column(db.Integer, primary_key=True, info='ID')
    engine_name = db.Column(db.String(100), nullable=False, info='数据库引擎名称')
    host = db.Column(db.String(100), nullable=False, info='数据库IP')
    port = db.Column(db.String(100), nullable=False, info='端口号')
    u_name = db.Column(db.String(100), nullable=False, info='用户名')
    password = db.Column(db.String(100), nullable=False, info='密码')
    db_name = db.Column(db.String(100), nullable=False, info='数据库名')
    create_time = db.Column(db.DateTime, info='添加时间')
    update_time = db.Column(db.DateTime, info='修改时间')
    is_delete = db.Column(db.Integer, info='是否删除')
