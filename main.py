# -*- coding: utf-8 -*-

import MySQLdb
import sqlite3
import psycopg2

from core import DataBase

#db = DataBase(provider=psycopg2, host='localhost',user='jm', passwd='root',db='jm')
#db = DataBase(provider=MySQLdb, host='localhost',user='root', passwd='root',db='jm')
db = DataBase(provider=sqlite3, db='MusicaInYou.db')

print [u.album for u in db.Table("Songs").filter("id > 15").
       filter("year = 2000").order_by("song").rows]

print [u.song for u in db.Table("Songs").filter("id = 1").rows]

print [c for c in db.Table("Songs").columns]


[u'essential selection vol. one', u'The Beatles 1', u'Please']
