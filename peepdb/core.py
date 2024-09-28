from tabulate import tabulate
import logging
from typing import Dict, Any
from datetime import date, time, datetime
from decimal import Decimal
from .db import MySQLDatabase, PostgreSQLDatabase, MariaDBDatabase, MongoDBDatabase, SQLiteDatabase

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
    elif db_type == 'sqlite':
        return SQLiteDatabase(host, user, password, database, **kwargs)
    else:
        raise ValueError("Unsupported database type")


def peep_db(db_type: str, host: str, user: str, password: str, database: str, table: str = None, format: str = 'table', page: int = 1, page_size: int = 100, scientific: bool = False) -> Any:
    print(f"peep_db called with: db_type={db_type}, host={host}, database={database}, table={table}, scientific={scientific}")
    db = connect_to_database(db_type, host, user, password, database)
    db.connect()
    try:
        if table:
            print(f"Fetching data for table: {table}")
            result = {table: db.fetch_data(table, page, page_size)}
        else:
            print("Fetching all tables")
            tables = db.fetch_tables()
            print(f"Tables fetched: {tables}")
            result = {table: db.fetch_data(table, page, page_size) for table in tables}

        if format == 'table':
            # Apply formatting to data for table output to adapt with scientific notation
            for table_name in result:
                for row in result[table_name]['data']:
                    for key in row:
                        row[key] = format_value(row[key], scientific, output_format='table')
            return format_as_table(result)
        else:
            # For JSON output, only convert date/time and Decimal types
            for table_name in result:
                for row in result[table_name]['data']:
                    for key in row:
                        if isinstance(row[key], (date, time, datetime)):
                            row[key] = row[key].isoformat()
                        elif isinstance(row[key], Decimal):
                            row[key] = float(row[key])
            return result
    finally:
        db.disconnect()


def format_as_table(data: Dict[str, Any]) -> str:
    formatted_result = []
    for table_name, table_data in data.items():
        formatted_result.append(f"Table: {table_name}")
        if table_data['data']:
            headers = table_data['data'][0].keys()
            table_rows = [list(row.values()) for row in table_data['data']]
            formatted_result.append(tabulate(table_rows, headers=headers, tablefmt='grid'))
        else:
            formatted_result.append("No data")
        formatted_result.append(
            f"Page {table_data['page']} of {table_data['total_pages']} (Total rows: {table_data['total_rows']})")
        formatted_result.append("")  # Add an empty line between tables
    return "\n".join(formatted_result).strip()


def format_value(value, scientific: bool, output_format: str):
    if isinstance(value, (date, time, datetime)):
        return value.isoformat()
    elif isinstance(value, Decimal):
        value = float(value)
    if output_format == 'json':
        return value
    elif isinstance(value, (int, float)):
        if scientific:
            return f"{value:.6e}"
        else:
            if abs(value) >= 1e6:
                if isinstance(value, float):
                    return f"{value:,.2f}"
                else:
                    return f"{value:,}"
            else:
                return str(value)
    else:
        return value