from tabulate import tabulate
import logging
from typing import Dict, Any
from .db import MySQLDatabase, PostgreSQLDatabase, MariaDBDatabase, MongoDBDatabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler for application logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)


def connect_to_database(db_type: str, host: str, user: str, password: str, database: str, **kwargs):
    if db_type == 'mysql':
        return MySQLDatabase(host, user, password, database, **kwargs)
    elif db_type == 'postgres':
        return PostgreSQLDatabase(host, user, password, database, **kwargs)
    elif db_type == 'mariadb':
        return MariaDBDatabase(host, user, password, database, **kwargs)
    elif db_type == 'mongodb':
        return MongoDBDatabase(host, user, password, database, **kwargs)
    else:
        raise ValueError("Unsupported database type")

def peep_db(db_type: str, host: str, user: str, password: str, database: str, table: str = None, format: str = 'table', page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    db = connect_to_database(db_type, host, user, password, database)
    db.connect()
    try:
        if table:
            result = {table: db.fetch_data(table, page, page_size)}
        else:
            tables = db.fetch_tables()
            result = {table: db.fetch_data(table, page, page_size) for table in tables}

        if format == 'table':
            return format_as_table(result)
        else:
            return result
    finally:
        db.disconnect()

def format_as_table(data: Dict[str, Any]) -> str:
    formatted_result = []
    for table_name, table_data in data.items():
        formatted_result.append(f"Table: {table_name}")
        if table_data['data']:
            headers = table_data['data'][0].keys()
            table_rows = [[row[col] for col in headers] for row in table_data['data']]
            formatted_result.append(tabulate(table_rows, headers=headers, tablefmt='grid'))
        else:
            formatted_result.append("No data")
        formatted_result.append(
            f"Page {table_data['page']} of {table_data['total_pages']} (Total rows: {table_data['total_rows']})")
        formatted_result.append("")  # Add an empty line between tables
    return "\n".join(formatted_result).strip()