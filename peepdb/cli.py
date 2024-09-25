import click
from .core import peep_db
from .config import get_connection, save_connection, list_connections, remove_connection, remove_all_connections
import json
from decimal import Decimal
from datetime import date

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
    peepDB: A Quick Database Table Viewer

    peepDB allows you to quickly inspect database tables without writing SQL queries.
    It supports MySQL, PostgreSQL, MariaDB, and SQLite.

    Commands:
      - view        View database tables
      - save        Save a new database connection
      - list        List saved connections
      - remove      Remove a specific saved connection
      - remove-all  Remove all saved connections

    Use 'peepdb COMMAND --help' for more information on a specific command.
    """
    pass

@cli.command()
@click.argument('connection_name')
@click.option('--db-type', type=click.Choice(['mysql', 'postgres', 'mariadb', 'sqlite']), required=True, help='Type of database (mysql, postgres, mariadb, sqlite)')
@click.option('--host', help='Database host (ignored for SQLite)')
@click.option('--user', help='Database user (ignored for SQLite)')
@click.option('--database', required=True, help='Database name or path for SQLite')
@click.option('--password', prompt=True, hide_input=True, required=False, help='Database password (required for non-SQLite databases)')
def save(connection_name, db_type, host, user, database, password):
    """
    Save a new database connection.

    Examples:

      Save a MySQL connection:
        peepdb save mymysql --db-type mysql --host localhost --user root --database mydb

      Save a SQLite connection:
        peepdb save sqlite1 --db-type sqlite --database /path/to/sample.db
    """
    if db_type == 'sqlite':
        password = None
        if host or user:
            click.echo("Warning: Host and user are ignored for SQLite connections.")
    else:
        if not host or not user:
            click.echo("Error: Host and user are required for non-SQLite databases.")
            return
        if not password:
            password = click.prompt('Enter database password', hide_input=True)
    
    try:
        save_connection(connection_name, db_type, host, user, password, database)
        click.echo(f"Connection '{connection_name}' saved successfully.")
    except Exception as e:
        click.echo(f"Error saving connection: {str(e)}")

@cli.command()
@click.argument('connection_name')
@click.option('--table', help='Specific table to view')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format (table or json)')
@click.option('--page', type=int, default=1, help='Page number for pagination')
@click.option('--page-size', type=int, default=100, help='Number of rows per page')
def view(connection_name, table, format, page, page_size):
    """
    View database tables.

    Examples:

      View all tables in a connection:
        peepdb view mymysql

      View a specific table with pagination:
        peepdb view mymysql --table users --page 2 --page-size 50

      Get the output in JSON format:
        peepdb view mymysql --format json
    """
    connection = get_connection(connection_name)
    if connection is None:
        click.echo(f"Error: No saved connection found with name '{connection_name}'.")
        return

    db_type, host, user, password, database = connection
    try:
        result = peep_db(
            db_type=db_type,
            host=host,
            user=user,
            password=password,
            database=database,
            table=table,
            format=format,
            page=page,
            page_size=page_size
        )

        if format == 'json':
            click.echo(result)
        else:
            click.echo(result)
            if table:
                click.echo(f"\nCurrent Page: {page}")
                # You might want to dynamically determine if there's a next or previous page based on total_pages
                # For simplicity, assuming a maximum of 100 pages
                if page < 100:
                    click.echo(f"Next Page: peepdb view {connection_name} --table {table} --page {page + 1} --page-size {page_size}")
                if page > 1:
                    click.echo(f"Previous Page: peepdb view {connection_name} --table {table} --page {page - 1} --page-size {page_size}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

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
def remove(connection_name):
    """
    Remove a specific saved connection.

    Example:
      peepdb remove mymysql
    """
    if remove_connection(connection_name):
        click.echo(f"Connection '{connection_name}' removed successfully.")
    else:
        click.echo(f"Error: Connection '{connection_name}' does not exist.")

@cli.command('remove-all')
def remove_all_cmd():
    """
    Remove all saved connections.

    Caution: This will delete all your saved database connections.

    Example:
      peepdb remove-all
    """
    count = remove_all_connections()
    click.echo(f"All {count} connections removed successfully.")

if __name__ == '__main__':
    cli()