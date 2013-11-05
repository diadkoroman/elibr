# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from core.dbconn import Base, metadata, dbc

assoc_table = Table('books_authors',metadata,
Column('book_id',Integer,ForeignKey('elibr_books.id')),
Column('author_id',Integer,ForeignKey('elibr_authors.id'))
)

class Book(Base):
    __tablename__ = 'elibr_books'
    id = Column(Integer,primary_key = True)
    nazva = Column(String)
    authors = relationship('Author',secondary=assoc_table,backref='books')

class Author(Base):
    __tablename__ = 'elibr_authors'
    id = Column(Integer,primary_key = True)
    imja = Column(String)

metadata.create_all(dbc)
