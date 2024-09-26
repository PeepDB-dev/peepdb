import pymysql
from .base import BaseDatabase
from typing import List, Dict, Any

class MariaDBDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port or 3306,
                cursorclass=pymysql.cursors.DictCursor,
                **self.extra_params
            )
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to MariaDB database: {self.database}")
        except pymysql.Error as e:
            self.logger.error(f"Error connecting to MariaDB database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info(f"Disconnected from MariaDB database: {self.database}")

    def fetch_tables(self) -> List[str]:
        self.cursor.execute("SHOW TABLES")
        return [list(table.values())[0] for table in self.cursor.fetchall()]

    def fetch_data(self, table: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        self.cursor.execute(f"SELECT COUNT(*) as total FROM {table}")
        total_rows = self.cursor.fetchone()['total']

        self.cursor.execute(f"SELECT * FROM {table} LIMIT {page_size} OFFSET {offset}")
        rows = self.cursor.fetchall()

        return {
            'data': rows,
            'page': page,
            'total_pages': (total_rows + page_size - 1) // page_size,
            'total_rows': total_rows
        }