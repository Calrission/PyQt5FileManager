from database.push_query_db_decorator import push_query_db_decorator
from sqlite3 import Cursor, Connection


class OpenTabsRequests:
    @push_query_db_decorator
    def get_all_open_tabs(self, cursor: Cursor, conn: Connection):
        result = cursor.execute("select * from open_tabs").fetchall()
        paths_points = [i[1] for i in result]
        return paths_points

    @push_query_db_decorator
    def add_open_tab(self, tab_path: str, cursor: Cursor, conn: Connection):
        cursor.execute(f"insert into open_tabs(path) values ('{tab_path}')")
        conn.commit()

    @push_query_db_decorator
    def remove_open_tab(self, tab_path: str, cursor: Cursor, conn: Connection):
        cursor.execute(f"delete from open_tabs where path='{tab_path}'")
        conn.commit()

    @push_query_db_decorator
    def update_open_tab(self, old_tab_path: str, new_tab_path: str, cursor: Cursor, conn: Connection):
        cursor.execute(f"update open_tabs set path='{new_tab_path}' where path='{old_tab_path}'")
        conn.commit()
