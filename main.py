# -*- coding: utf-8 -*-

import MySQLdb
import sqlite3
import psycopg2

from core import DataBase

db = DataBase(provider=psycopg2, host='localhost',user='jm', passwd='root',db='jm')
#db = DataBase(provider=MySQLdb, host='localhost',user='root', passwd='root',db='jm')
#db = DataBase(provider=sqlite3, db='jm.db')

print [u.name for u in db.Table("Person").filter("age > 15").
       filter("name = 'jm'").order_by("name").rows]

print [u.name for u in db.Table("Person").rows]

print [c for c in db.Table("Person").columns]
