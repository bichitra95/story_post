

import maya
from decimal import Decimal

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()


def get_current_ist_time():
    return maya.now().datetime(to_timezone='Asia/Kolkata', naive=True)


class Common(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.TIMESTAMP, default=get_current_ist_time, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=get_current_ist_time, onupdate=get_current_ist_time, nullable=False)
    performed_by = db.Column(db.Integer, nullable=True)
    row_status = db.Column(db.String(length=20), default='active', nullable=False)
    @classmethod
    def new(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        return obj

    @classmethod
    def get(cls, *args):
        return db.session.query(cls).filter(*args).first()

    @classmethod
    def get_all(cls, *args):
        return db.session.query(cls).filter(*args).all()

    def as_dict(self, datetime_to_str=True):
        return {c.name: getattr(self, c.name).isoformat() if isinstance(getattr(self, c.name),
                                                                        datetime) and datetime_to_str else float(
            getattr(self, c.name)) if isinstance(getattr(self, c.name), Decimal) else getattr(self, c.name) for c in
                self.__table__.columns}


class UserIdentities(Common):
    __tablename__ = 'author_identities'
    identity = db.Column(db.String(length=255), nullable=False)
    name = db.Column(db.String(length=150), nullable=False)
    identity_type = db.Column(db.String(length=50), nullable=False)
    password = db.Column(db.String(length=100), nullable=False)
    row_status = db.Column(db.String(length=20) , default='active' , nullable=False)
    __table_args__ = (Index('index_on_identity_v3_user_identity',
                            identity, row_status, unique=True,
                            postgresql_where=row_status == 'active'),)


class Stories(Common):
    __tablename__ = 'stories_library'
    draft = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(length=150), nullable=False)
    tags = db.Column(JSONB, nullable=True)
    if_publiced = db.Column(db.Boolean, nullable=True)
