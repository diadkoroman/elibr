# -*- coding: utf-8 -*-
import re
from wtforms import Form, TextField, PasswordField,validators

class SearchForm(Form):
    searchf = TextField('Пошук',[
    validators.required(),
    validators.Regexp(regex='^[^~`#$^&*\.,]+$',flags=re.I+re.U,message='Це поле не може містити спеціальних символів!'),
    validators.Length(min=3,max=50,message='Довжина введеного рядка повинна бути від %(min) до %(max)')
    ])
