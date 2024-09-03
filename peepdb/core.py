import mysql.connector
import psycopg2
import pymysql
from decimal import Decimal
from datetime import date, time, datetime
from tabulate import tabulate

def connect_to_database(db_type, host, user, password, database):
    if db_type == 'mysql':
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    elif db_type == 'postgres':
        return psycopg2.connect(host=host, user=user, password=password, database=database)
    elif db_type == 'mariadb':
        return pymysql.connect(host=host, user=user, password=password, database=database)
    else:
        raise ValueError("Unsupported database type")

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