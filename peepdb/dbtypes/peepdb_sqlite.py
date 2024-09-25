import sqlite3


def connect_to_db(database):
    return sqlite3.connect(database)


def fetch_tables(cursor):
    return cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
