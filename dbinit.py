# -*- coding: utf-8 -*-
import os,sys,sqlite3
from contextlib import closing

CWD = os.getcwd()
DB_FILE='elibrary.db'
DB_PATH = CWD+'/assets/db/'+DB_FILE

DCHEMA_FILE = 'elibrary.sql'
DSCHEMA_PATH = CWD+'/assets/schema/'+DCHEMA_FILE

def connect_db():
    if sqlite3:
        return sqlite3.connect(DB_PATH)

def fill_db():
    with closing(connect_db()) as db:
        with open(DSCHEMA_PATH) as f:
            db.cursor().executescript(f.read())
            db.commit()

def main():
    print  '''
            **************************
            *         Вітання        *
            **************************
           '''
    command = raw_input('Бажаєте заповнити БД? (y/n)')
    if command =='y':
        fill_db()


if __name__ == '__main__':
    main()
