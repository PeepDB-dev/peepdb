import mysql.connector
import psycopg2
import pymysql
from decimal import Decimal
from datetime import date, time, datetime
from tabulate import tabulate
import logging
import math

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

def view_table(cursor, table_name, page=1, page_size=100):
    # Get total number of rows
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cursor.fetchone()[0]
    
    # Calculate total pages
    total_pages = math.ceil(total_rows / page_size)
    
    # Ensure page is within bounds
    page = max(1, min(page, total_pages))
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Fetch data for the current page
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}")
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
    
    return {
        'data': rows,
        'page': page,
        'total_pages': total_pages,
        'total_rows': total_rows
    }

def peep_db(db_type, host, user, password, database, table=None, format='table', page=1, page_size=100):
    conn = connect_to_database(db_type, host, user, password, database)
    cursor = conn.cursor()

    if table:
        result = {table: view_table(cursor, table, page, page_size)}
    else:
        tables = fetch_tables(cursor, db_type)
        result = {table: view_table(cursor, table, page, page_size) for table in tables}

    cursor.close()
    conn.close()

    if format == 'table':
        return format_as_table(result)
    else:
        return result

def format_as_table(data):
    formatted_result = []
    for table_name, table_data in data.items():
        formatted_result.append(f"Table: {table_name}")
        if table_data['data']:
            headers = table_data['data'][0].keys()
            table_rows = [[row[col] for col in headers] for row in table_data['data']]
            formatted_result.append(tabulate(table_rows, headers=headers, tablefmt='grid'))
        else:
            formatted_result.append("No data")
        formatted_result.append(f"Page {table_data['page']} of {table_data['total_pages']} (Total rows: {table_data['total_rows']})")
        formatted_result.append("")  # Add an empty line between tables
    return "\n".join(formatted_result).strip()