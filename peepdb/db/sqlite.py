import os
import sqlite3
from .base import BaseDatabase
from typing import List, Dict, Any

class SQLiteDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            print(f"Attempting to connect to SQLite database.")
            print(f"Self.host: {self.host}")
            print(f"Self.database: {self.database}")
            self.db_path = os.path.abspath(self.host)
            print(f"Using database file: {self.db_path}")
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print(f"Connected to SQLite database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print(f"Disconnected from SQLite database: {self.db_path}")

    def fetch_tables(self) -> List[str]:
        print("Fetching tables from SQLite database")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Database file path: {self.db_path}")
        
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in self.cursor.fetchall()]
            print(f"Tables found: {tables}")
            return tables
        except sqlite3.Error as e:
            print(f"Error when querying the database: {e}")
            return []

    def fetch_data(self, table: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        print(f"Fetching data from table '{table}' (page: {page}, page_size: {page_size})")
        offset = (page - 1) * page_size
        try:
            self.cursor.execute(f"SELECT COUNT(*) as total FROM '{table}'")
            total_rows = self.cursor.fetchone()[0]
            print(f"Total rows in table '{table}': {total_rows}")

            self.cursor.execute(f"SELECT * FROM '{table}' LIMIT {page_size} OFFSET {offset}")
            rows = [dict(row) for row in self.cursor.fetchall()]
            print(f"Fetched {len(rows)} rows from table '{table}'")

            return {
                'data': rows,
                'page': page,
                'total_pages': (total_rows + page_size - 1) // page_size,
                'total_rows': total_rows
            }
        except sqlite3.Error as e:
            print(f"Error fetching data from table '{table}': {e}")
            raise