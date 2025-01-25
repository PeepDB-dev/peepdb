import oracledb
from typing import List, Dict, Any
from .base import BaseDatabase
import logging


class OracleDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            self.connection = oracledb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                service_name=self.database,
                port=self.port or 1521,
                **self.extra_params,
            )
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to Oracle database: {self.database}")

        except oracledb.Error as e:
            self.logger.error(f"Error connecting to Oracle database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info(f"Disconnected from Oracle database: {self.database}")

    def fetch_tables(self) -> List[str]:
        self.cursor.execute("SELECT table_name FROM user_tables")
        return [table[0] for table in self.cursor.fetchall()]

    def fetch_data(
        self, table: str, page: int = 1, page_size: int = 100
    ) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        self.cursor.execute(f"SELECT COUNT(*) as total FROM {table}")
        total_rows = self.cursor.fetchone()[0]

        self.cursor.execute(
            f"SELECT * FROM {table} OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"
        )
        rows = self.cursor.fetchall()

        column_names = [description[0] for description in self.cursor.description]

        formatted_rows = [dict(zip(column_names, row)) for row in rows]

        return {
            "data": formatted_rows,
            "page": page,
            "total_pages": (total_rows + page_size - 1) // page_size,
            "total_rows": total_rows,
        }
