import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rate = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
