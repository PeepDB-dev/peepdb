import mysql.connector
from .base import BaseDatabase
from typing import List, Dict, Any

class MySQLDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port or 3306,
                **self.extra_params
            )
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info(f"Connected to MySQL database: {self.database}")
        except mysql.connector.Error as e:
            self.logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info(f"Disconnected from MySQL database: {self.database}")

    def fetch_tables(self) -> List[str]:
        self.cursor.execute("SHOW TABLES")
        return [table['Tables_in_' + self.database] for table in self.cursor.fetchall()]

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