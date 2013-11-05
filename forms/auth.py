# -*- coding: utf-8 -*-
from wtforms import Form, TextField, PasswordField,validators

class AutForm(Form):
    u_login = TextField('Логін'.decode('UTF-8'),[validators.required()])
    u_passw = PasswordField('Пароль'.decode('UTF-8'),[validators.required()])

class RegForm(Form):
    r_login = TextField('Введіть Ваш нік'.decode('UTF-8'),[validators.required()])
    r_passw = PasswordField('Введіть пароль для входу'.decode('UTF-8'),[validators.required(),validators.EqualTo('rep_r_passw',message='Паролі повинні співпадати!'.decode('UTF-8'))])
    rep_r_passw = PasswordField('Повторіть пароль'.decode('UTF-8'),[validators.required()])
