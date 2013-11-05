# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime
from core.dbconn import Base, metadata, dbc

class Elibr_User(Base):
    __tablename__ = 'elibr_users'
    id = Column(Integer,primary_key = True)
    nickname = Column(String)
    password = Column(Text)

metadata.create_all(dbc)
