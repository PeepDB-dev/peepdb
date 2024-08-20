import mysql.connector
import psycopg2
import pymysql
from decimal import Decimal

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
            row_dict[columns[i]] = value
        rows.append(row_dict)
    return rows

def peep_db(db_type, host, user, password, database, table=None):
    conn = connect_to_database(db_type, host, user, password, database)
    cursor = conn.cursor()

    if table:
        result = {table: view_table(cursor, table)}
    else:
        tables = fetch_tables(cursor, db_type)
        result = {table: view_table(cursor, table) for table in tables}

    cursor.close()
    conn.close()

    return result