# -*- coding: utf-8 -*-

import MySQLdb
import sqlite3
import psycopg2

class DataBase(object):

    def __init__(self, provider, host='', user='', passwd='', db=''):

        self.provider = provider

        self.connections = {MySQLdb : self.get_mysql_connection,
                            sqlite3 : self.get_sqlite_connection,
                            psycopg2 : self.get_postgre_connection,}

        self.connections[provider](host, user, passwd, db)
        self.cursor = self.db.cursor()

        self.providers = {MySQLdb : self.get_mysql_columns,
                          sqlite3 : self.get_sqlite_columns,
                          psycopg2 : self.get_postgre_columns,}

    def get_mysql_connection(self, host='', user='', passwd='', db=''):
        self.db = self.provider.connect(host=host, user=user, passwd=passwd, db=db)

    def get_postgre_connection(self, host='', user='', passwd='', db=''):
        self.db = self.provider.connect(host=host, user=user, password=passwd, database=db)

    def get_sqlite_connection(self, host='', user='', passwd='', db=''):
        self.db = self.provider.connect(db)

    def get_mysql_columns(self, name):

        self.sql_rows = 'Select * From %s' % name
        sql_columns = "describe %s" % name
        self.cursor.execute(sql_columns)
        return [row[0] for row in self.cursor.fetchall()]

    def get_sqlite_columns(self, name):

        self.sql_rows = 'Select * From %s' % name
        sql_columns = "PRAGMA table_info(%s)" % name
        self.cursor.execute(sql_columns)
        return [row[1] for row in self.cursor.fetchall()]

    def get_postgre_columns(self, name):

        self.sql_rows = 'Select * From "%s"' % name
        sql_columns = """select column_name
                        from information_schema.columns
                        where table_name = '%s';""" % name
        self.cursor.execute(sql_columns)
        return [row[0] for row in self.cursor.fetchall()]

    def Table(self, name):

        columns = self.providers[self.provider](name)
        return Query(self.cursor, self.sql_rows, columns, name)


class Query(object):

    def __init__(self, cursor, sql_rows, columns, name):
        self.cursor = cursor
        self.sql_rows = sql_rows
        self.columns = columns
        self.name = name

    def filter(self, criteria):

        key_word = "AND" if "WHERE" in self.sql_rows else "WHERE"
        sql = self.sql_rows + " %s %s" % (key_word, criteria)
        return Query(self.cursor, sql, self.columns, self.name)

    def order_by(self, criteria):
        return Query(self.cursor, self.sql_rows + " ORDER BY %s" % criteria, self.columns, self.name)

    def group_by(self, criteria):
        return Query(self.cursor, self.sql_rows + " GROUP BY %s" % criteria, self.columns, self.name)

    def get_rows(self):
        print self.sql_rows
        columns = self.columns
        self.cursor.execute(self.sql_rows)
        return [Row(zip(columns, fields), self.name) for fields in self.cursor.fetchall()]

    rows = property(get_rows)


class Row(object):

    def __init__(self, fields, table_name):

        self.__class__.__name__ = table_name + "_Row"

        for name, value in fields:
            setattr(self, name, value)

