# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from website.main import app
from website.main import db


# db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, info='主键，用户ID')
    user_name = db.Column(db.String(50), nullable=False, unique=True, info='用户名/姓名')
    email = db.Column(db.String(50), nullable=False, info='邮箱')
    create_time = db.Column(db.DateTime, nullable=False, info='创建时间，精确到秒')
    nick_name = db.Column(db.String(50), info='昵称')
    phone = db.Column(db.String(20), info='手机号')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除，0-正常，1-删除')


if __name__ == '__main__':

    u = User.query.first()
    # for u in uu:
    #     print(u.id, u.email, u.phone, u.nick_name)
    # u = uu[0]
    print(u.id, u.email, u.phone, u.nick_name)

    # user2 = User(user_name="test1",
    #              email = "test1@df.com",create_time="2021-07-30 15:52:55", nick_name="nick_test", phone="13049164685")
    # db.session.add(user2)
    # db.session.commit()
