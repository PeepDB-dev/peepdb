import mysql.connector


def connect_to_db(host, user, password, database, port, **kwargs):
    """
    Establishes a connection to database using the provided parameters.

    Args:
        host (str): The hostname or IP address of the server.
        user (str): The username to use for the connection.
        password (str): The password associated with the username.
        database (str): The name of the database to connect to.
        port (int): The port number on which the server is listening. Defaults to 3306 if not provided.

    Returns:
        mysql.connector.MySQLConnection: A MySQL connection object.

    Raises:
        mysql.connector.Error
    """
    return mysql.connector.connect(host=host, user=user, password=password, database=database, port=port or 3306,
                                   **kwargs)


def fetch_tables(cursor):
    """
    Retrieves the list of tables in the current database.

    Args:
        cursor (mysql.connector.cursor): Cursor object used to execute SQL queries.

    Returns:
        list of tuple: A list of tuples where each tuple contains the name of a table in the database.

    Raises:
        mysql.connector.Error
    """
    cursor.execute("SHOW TABLES")
    return cursor.fetchall()

