from sqlite3 import connect
from values.ConstValues import DATABASE_NAME


def push_query_db_decorator(fun):
    def push_query_db(*args):
        with connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            return fun(*args, cursor=cursor, conn=conn)
    return push_query_db
