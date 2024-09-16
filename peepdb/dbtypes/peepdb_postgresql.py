import psycopg2


def connect_to_db(host, user, password, database, port, **kwargs):
    """
    Establishes a connection to database using the provided credentials.

    Args:
        host (str): The hostname or IP address of the server.
        user (str): The username to use for the connection.
        password (str): The password associated with the username.
        database (str): The name of the database to connect to.
        port (int): The port number on which the server is listening. Defaults to 5432 if not provided.

    Returns:
        psycopg2.extensions.connection: A connection object to the database.

    Raises:
        psycopg2.OperationalError
    """
    return psycopg2.connect(host=host, user=user, password=password, database=database, port=port or 5432,
                            **kwargs)


def fetch_tables(cursor):
    """
    Retrieves the list of tables in the current database.

    Args:
        cursor (psycopg2.extensions.cursor): Cursor object used to execute SQL queries.

    Returns:
        list of tuple: A list of tuples where each tuple contains the name of a table in the database.

    Raises:
        psycopg2.Error
    """
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return cursor.fetchall()

