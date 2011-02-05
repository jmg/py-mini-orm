# -*- coding: utf-8 -*-
import MySQLdb

class DataBase(object):

    def __init__(self, host='', user='', passwd='', db=''):

        self.db = MySQLdb.connect(host, user, passwd, db)
        self.cursor = self.db.cursor()

    def Table(self, name):

        return Table(name, self.cursor)


class Table(object):

    def __init__(self, name, cursor):

        self.name = name
        self.cursor = cursor

        cursor.execute("describe %s" % name)
        self.columns = [row[0] for row in cursor.fetchall()]

        self.sql = "Select * From %s" % name

    def filter(self, criteria):
        return RowList(self, self.sql).filter(criteria)


class RowList(list):

    def get_rows(self):
        print self.sql
        self.table.cursor.execute(self.sql)
        return [Row(self.table.columns, fields, self.table.name) for fields in self.table.cursor.fetchall()]

    rows = property(get_rows)

    def __init__(self, table, sql):
        self.sql = sql
        self.table = table

    def filter(self, criteria):
        if "WHERE" in self.sql:
            key_word = "AND"
        else:
            key_word = "WHERE"
        sql = self.sql + " %s %s" % (key_word, criteria)
        return RowList(self.table, sql)

    def order_by(self, criteria):
        return RowList(self.table, self.sql + " ORDER BY %s" % criteria)

    def group_by(self, criteria):
        return RowList(self.table, self.sql + " GROUP BY %s" % criteria)


class Row(object):

    def __init__(self, names, fields, table_name):

        self.__class__.__name__ = table_name

        i = 0
        for name in names:
            setattr(self, name, fields[i])
            i += 1

