# -*- coding: utf-8 -*-
from flask import session
from randomize import secretkey

#генератор csrf
def gen_csrf_token(check_key='_csrf_sess',key_length=64):
    if not check_key in session:
        skey=secretkey(key_length)
        session[check_key]=''.join(secretkey(key_length))
    return session[check_key]
    
