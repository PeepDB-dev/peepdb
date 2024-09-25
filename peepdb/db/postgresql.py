import psycopg2
from psycopg2.extras import RealDictCursor
from .base import BaseDatabase
from typing import List, Dict, Any

class PostgreSQLDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.database,
                port=self.port or 5432,
                **self.extra_params
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.logger.info(f"Connected to PostgreSQL database: {self.database}")
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info(f"Disconnected from PostgreSQL database: {self.database}")

    def fetch_tables(self) -> List[str]:
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        return [table['table_name'] for table in self.cursor.fetchall()]

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