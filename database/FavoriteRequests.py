from sqlite3 import Cursor, Connection
from database.push_query_db_decorator import push_query_db_decorator


class FavoriteRequests:
    @push_query_db_decorator
    def get_favorites(self, cursor: Cursor, conn: Connection):
        result = cursor.execute("select * from favorites").fetchall()
        return [i[1] for i in result]

    @push_query_db_decorator
    def add_favorite(self, path: str, cursor: Cursor, conn: Connection):
        cursor.execute(f"insert into favorites(path) values('{path}')")
        conn.commit()

    @push_query_db_decorator
    def remove_favorite(self, path: str, cursor: Cursor, conn: Connection):
        cursor.execute(f"delete from favorites where path='{path}'")
        conn.commit()
