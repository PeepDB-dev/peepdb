import mysql.connector
import psycopg2
import pymysql
from decimal import Decimal
from datetime import date, time, datetime
from tabulate import tabulate
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def connect_to_database(db_type, host, user, password, database, port=None, **kwargs):
       logger.debug(f"Attempting to connect to {db_type} database '{database}' on host '{host}' with user '{user}'")
       try:
           if db_type == 'mysql':
               conn = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port or 3306, **kwargs)
           elif db_type == 'postgres':
               conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=port or 5432, **kwargs)
           elif db_type == 'mariadb':
               conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port or 3306, **kwargs)
           else:
               raise ValueError("Unsupported database type")
           logger.debug("Connection successful")
           return conn
       except (mysql.connector.Error, psycopg2.Error, pymysql.Error) as e:
           logger.error(f"Failed to connect to {db_type} database: {str(e)}")
           raise ConnectionError(f"Failed to connect to {db_type} database: {str(e)}")
    
def fetch_tables(cursor, db_type):
    if db_type in ['mysql', 'mariadb']:
        cursor.execute("SHOW TABLES")
    elif db_type == 'postgres':
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return [table[0] for table in cursor.fetchall()]

def view_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    rows = []
    for row in cursor.fetchall():
        row_dict = {}
        for i, value in enumerate(row):
            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, (date, time, datetime)):
                value = value.isoformat()
            row_dict[columns[i]] = value
        rows.append(row_dict)
    return rows

def peep_db(db_type, host, user, password, database, table=None, format='table'):
    conn = connect_to_database(db_type, host, user, password, database)
    cursor = conn.cursor()

    if table:
        result = {table: view_table(cursor, table)}
    else:
        tables = fetch_tables(cursor, db_type)
        result = {table: view_table(cursor, table) for table in tables}

    cursor.close()
    conn.close()

    if format == 'table':
        return format_as_table(result)
    else:
        return result

def format_as_table(data):
    formatted_result = []
    for table_name, rows in data.items():
        formatted_result.append(f"Table: {table_name}")
        if rows:
            headers = rows[0].keys()
            table_data = [[row[col] for col in headers] for row in rows]
            formatted_result.append(tabulate(table_data, headers=headers, tablefmt='grid'))
        else:
            formatted_result.append("No data")
        formatted_result.append("")  # Add an empty line between tables
    return "\n".join(formatted_result).strip()  # Remove trailing newline