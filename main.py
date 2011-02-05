# -*- coding: utf-8 -*-

from core import DataBase

db = DataBase(host='localhost',user='root', passwd='root',db='pylinq')

print [u.name for u in db.Table("users").filter("age > 15").filter("name = 'jm'").group_by("name").order_by("name").rows]

print [c for c in db.Table("users").columns]
