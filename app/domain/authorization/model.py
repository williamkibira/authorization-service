from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database.base import BaseModel


class Role(BaseModel):
    __tablename__ = 'role_tb'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    index = Column('idx', Integer)


association_table = Table('user_roles', BaseModel.metadata,
                          Column('user_id', Integer, ForeignKey('user_tb.id'), primary_key=True),
                          Column('role_id', Integer, ForeignKey('role_tb.id'), primary_key=True)
                          )


class User(BaseModel):
    __tablename__ = 'user_tb'
    id = Column('id', Integer, primary_key=True)
    identifier = Column('identifier', String)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    email_address = Column('email_address', String)
    photo_identifier = Column('photo_identifier', String)
    password = Column('password', String)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    index = Column('idx', Integer)
    roles = relationship(Role,
                         secondary=association_table,
                         backref="users")

