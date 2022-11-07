from database.InitorRequests import push_query_db_decorator
from sqlite3 import Cursor, Connection


class CountOpenRequests:
    @push_query_db_decorator
    def get_all_dict_desc(self, cursor: Cursor, conn: Connection):
        result = cursor.execute("select * from count_open order by count desc").fetchall()
        return {i[1]: i[2] for i in result}

    def get_all_dict_limit(self, limit: int):
        return self.get_all_dict_desc()[:limit]

    def get_max_count_path(self):
        data = self.get_all_dict_desc()
        return list(data.keys())[0]

    @push_query_db_decorator
    def update_count(self, path: str, new_count: int, cursor: Cursor, conn: Connection):
        cursor.execute(f"update count_open set count={new_count} where path='{path}'")
        conn.commit()

    def update_count_plus_one(self, path: str):
        count = self.get_count(path) + 1
        self.update_count(path, count)

    @push_query_db_decorator
    def get_count(self, path: str, cursor: Cursor, conn: Connection):
        result = cursor.execute(f"select count from count_open where path='{path}'").fetchall()
        return result[0][0]
