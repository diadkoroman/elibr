# -*- coding: utf-8 -*-
from wtforms import Form, TextField, IntegerField, SelectMultipleField, validators
from models.library import Book, Author
from core.dbconn import sess


class AddEntryForm(Form):

    addtype = TextField('',[validators.required(),validators.Length(min=3,max=20)])
    add = TextField('',[validators.required(),validators.Length(min=3,max=150)])
    authors_list = SelectMultipleField('Автори'.decode('UTF-8'))
    books_list = SelectMultipleField('Книги'.decode('UTF-8'))
    #add_books_author = TextField('Додати автора (якщо немає у списку)'.decode('UTF-8'),[validators.required(),validators.Length(min=3,max=150)])
    #add_authors_book = TextField('Додати книгу (якщо немає у списку)'.decode('UTF-8'),[validators.required(),validators.Length(min=3,max=150)])


class UpdateEntryForm(Form):
    edittype = TextField('',[validators.required(),validators.Length(min=3,max=20)])
    upd = TextField('',[validators.required(),validators.Length(min=3,max=150)])
    upd_id = IntegerField('',[validators.required()])
    authors_list = SelectMultipleField('Автори'.decode('UTF-8'))
    books_list = SelectMultipleField('Книги'.decode('UTF-8'))
