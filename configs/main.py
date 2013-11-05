# -*- coding: utf-8 -*-
import os

################## db #################################
SQLITE_DB_NAME='elibrary.db'
SQLITE_DB_DIRPATH=os.environ['project_dir']+'/'+'assets/db'
SQLITE_DB_FULLPATH=SQLITE_DB_DIRPATH+'/'+SQLITE_DB_NAME

SQLITE_SCHEMA_NAME='elibrary.sql'
SQLITE_SCHEMA_DIRPATH=os.environ['project_dir']+'/'+'assets/schema'
SQLITE_SCHEMA_FULLPATH=SQLITE_SCHEMA_DIRPATH+'/'+SQLITE_SCHEMA_NAME
########################################################

################## others ##############################
PAGENAME = 'Elibr'
PAGETITLE = PAGENAME
########################################################
