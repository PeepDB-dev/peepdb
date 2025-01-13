import pyodbc
from .base import BaseDatabase
from typing import List, Dict, Any
import logging

class MSSQLDatabase(BaseDatabase):
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 1433, trusted: bool = False, **kwargs):
        super().__init__(host, user, password, database, port, **kwargs)
        self.trusted = trusted
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        driver = '{ODBC Driver 17 for SQL Server}'
        server = f"{self.host},{self.port}" if self.port else self.host
        if self.trusted:
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={self.database};Trusted_Connection=yes;"
        else:
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={self.database};UID={self.user};PWD={self.password};"
        self.logger.debug(f"Connection String: {connection_string}")
        try:
            self.connection = pyodbc.connect(connection_string, autocommit=False)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to MSSQL database: {self.database}")
        except pyodbc.Error as e:
            self.logger.error(f"Error connecting to MSSQL database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info(f"Disconnected from MSSQL database: {self.database}")

    def fetch_tables(self) -> List[str]:
        # Get both schema and table name
        self.cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        # Return something like "schemaName.tableName"
        return [f"{row[0]}.{row[1]}" for row in self.cursor.fetchall()]

    def fetch_data(self, table: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        # Count total rows
        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_rows = self.cursor.fetchone()[0]

        # Fetch data using OFFSET FETCH
        self.cursor.execute(f"""
            SELECT * FROM {table}
            ORDER BY (SELECT NULL)
            OFFSET {offset} ROWS
            FETCH NEXT {page_size} ROWS ONLY;
        """)
        columns = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        return {
            'data': data,
            'page': page,
            'total_pages': (total_rows + page_size - 1) // page_size,
            'total_rows': total_rows
        }
