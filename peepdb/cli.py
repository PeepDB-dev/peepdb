import click
import json
from .core import peep_db
from .config import (
    get_connection,
    save_connection,
    list_connections,
    remove_connection,
    remove_all_connections
)
from .exceptions import InvalidPassword
from decimal import Decimal
from datetime import date
import logging

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, date):
            return obj.isoformat()
        return super(CustomEncoder, self).default(obj)


@click.group()
@click.version_option()
def cli():
    """
    peepDB: A quick database table viewer.

    This tool allows you to quickly inspect database tables without writing SQL queries.
    It supports MySQL, PostgreSQL, MariaDB, SQLite, MongoDB, Firebase, MSSQL, and OracleDB.

    Usage examples:

    1. Save a new database connection:
       peepdb save postgres1 --db-type postgres --host localhost --user postgres --password YourPassword --database peepdb_test

    2. View all tables in a saved connection:
       peepdb view postgres1

    3. View a specific table with pagination:
       peepdb view postgres1 --table users --page 2 --page-size 50

    4. Remove a saved connection:
       peepdb remove postgres1

    Use 'peepdb COMMAND --help' for more information on a specific command.
    """
    pass


@cli.command()
@click.argument('connection_name')
@click.option('--db-type',
              type=click.Choice(['mysql', 'postgres', 'mariadb', 'sqlite', 'mongodb', 'firebase', 'mssql', 'oracle']),
              required=True,
              help='Database type')
@click.option('--host', required=True, help='Database host or file path for SQLite')
@click.option('--port', type=int, required=False, help='Database port (optional)')
@click.option('--user', required=False, help='Database user (not required for SQLite)')
@click.option('--password', required=False, help='Database password (not required for SQLite)')
@click.option('--database', required=False, help='Database name (not required for SQLite/Firebase/MSSQL)')
@click.option('--trusted', is_flag=True, help='Use Windows Authentication (Trusted Connection) for MSSQL')
def save(connection_name, db_type, host, port, user, password, database, trusted):
    """
    Save a new database connection.

    Example:
    peepdb save test_conn --db-type mssql --host localhost --port 1433 --trusted --database SomeDB
    """
    if trusted:
        # For Windows Authentication, we skip user/password
        user = ''
        password = ''
    elif db_type not in ['sqlite', 'firebase']:
        if not user:
            user = click.prompt('Enter username')
        if not password:
            password = click.prompt('Enter password', hide_input=True, confirmation_prompt=True)

    save_connection(connection_name, db_type, host, port, user, password, database, trusted)
    click.echo(f"Connection '{connection_name}' saved successfully.")


@cli.command()
def list():
    """
    List saved connections.

    Example:
    peepdb list
    """
    list_connections()


@cli.command()
@click.argument('connection_name')
@click.confirmation_option(prompt='Are you sure you want to remove this connection?')
def remove(connection_name):
    """
    Remove a specific saved connection.

    Example:
    peepdb remove mydb
    """
    if remove_connection(connection_name):
        click.echo(f"Connection '{connection_name}' has been removed.")
    else:
        click.echo(f"No connection named '{connection_name}' found.")


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to remove ALL saved connections?')
def remove_all():
    """
    Remove all saved connections.

    Example:
    peepdb remove-all
    """
    count = remove_all_connections()
    click.echo(f"{count} connection(s) have been removed.")


@cli.command()
@click.argument('connection_name')
@click.option('--table', required=False, help='Specific table to view')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
@click.option('--page', type=int, default=1, help='Page number to view')
@click.option('--page-size', type=int, default=50, help='Number of rows per page')
@click.option('--scientific', is_flag=True, help='Use scientific notation for numbers')
def view(connection_name, table, format, page, page_size, scientific):
    """
    View data from a saved connection.

    Example:
    peepdb view mydb --table SomeTable
    """
    try:
        connection = get_connection(connection_name)
    except InvalidPassword:
        click.echo("Error: Unable to decrypt saved connection. Invalid password provided.")
        raise SystemExit(1)
    if not connection:
        click.echo(f"Error: No saved connection found with name '{connection_name}'.")
        return

    # If there's a sixth item, it's 'trusted'
    if len(connection) == 6:
        db_type, host, user, password, database, trusted = connection
    else:
        db_type, host, user, password, database = connection
        trusted = False

    result = peep_db(
        db_type=db_type,
        host=host,
        user=user,
        password=password,
        database=database,
        table=table,
        format=format,
        page=page,
        page_size=page_size,
        scientific=scientific,
        trusted=trusted
    )

    if format == 'table':
        click.echo(result)
        if table:
            click.echo("\nNavigation:")
            click.echo(f"Current Page: {page}")
            click.echo(f"Next Page: peepdb view {connection_name} --table {table} --page {page + 1} --page-size {page_size}")
            click.echo(f"Previous Page: peepdb view {connection_name} --table {table} --page {max(1, page - 1)} --page-size {page_size}")
    else:
        click.echo(json.dumps(result, indent=2, cls=CustomEncoder))


def main():
    cli()


if __name__ == '__main__':
    main()
