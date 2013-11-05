# -*- coding: utf-8 -*-
import random

rstr = 'qQwWeErRtTyYuUiIoOpPaAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM1234567890?~!@#$%^&*_+='
RAND_ITEMS=rstr * 5
DEFAULT_SECRETKEY_LENGTH=24

def secretkey(key_length=None):
    if key_length and isinstance(key_length,(int,)):
        sk=random.sample(RAND_ITEMS,key_length)
    else:
        sk=random.sample(RAND_ITEMS,DEFAULT_SECRETKEY_LENGTH)
    return sk
