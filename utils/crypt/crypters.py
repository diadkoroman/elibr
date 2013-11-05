# -*- coding: utf-8 -*-
import hashlib

#зашифрувати елемент
def encrypt_sha224(obj=None):
    return hashlib.sha224(obj).hexdigest()
    
        
