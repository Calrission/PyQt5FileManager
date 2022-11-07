from database.InitorRequests import push_query_db_decorator
from sqlite3 import Cursor, Connection


class EnterPointsRequests:
    @push_query_db_decorator
    def get_all_enter_points(self, cursor: Cursor, conn: Connection):
        result = cursor.execute("select * from enter_points").fetchall()
        paths_points = [i[1] for i in result]
        return paths_points
