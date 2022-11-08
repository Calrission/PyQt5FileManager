import sqlite3
from sqlite3 import connect, Connection, Cursor
from values.ConstValues import DATABASE_NAME


def push_query_db_decorator(fun):
    def push_query_db(*args):
        with connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            return fun(*args, cursor=cursor, conn=conn)
    return push_query_db


class InitorRequests:
    def __init__(self):
        self.tables = ["open_tabs"]

    def init_all_tables(self):
        for table in self.tables:
            try:
                self.get_fun_init_table(table)(self)
            except sqlite3.OperationalError as e:
                pass

    @staticmethod
    def get_fun_init_table(name_table: str):
        if name_table == "open_tabs":
            return InitorRequests.create_table_open_tabs
        elif name_table == "favorites":
            return InitorRequests.create_table_favorites

    @push_query_db_decorator
    def create_table_open_tabs(self, cursor: Cursor, conn: Connection):
        cursor.execute("create table 'open_tabs' (id INTEGER NOT NULL PRIMARY KEY, path STRING NOT NULL)")
        conn.commit()

    @push_query_db_decorator
    def create_table_favorites(self, cursor: Cursor, conn: Connection):
        cursor.execute("create table 'favorites' (id INTEGER NOT NULL PRIMARY KEY, path STRING NOT NULL)")
        conn.commit()
