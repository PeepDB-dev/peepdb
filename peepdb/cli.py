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
    peepDB: A quick database table viewer.

    This tool allows you to quickly inspect database tables without writing SQL queries.
    It supports MySQL, PostgreSQL, and MariaDB.

    Commands:
    - view: View database tables
    - save: Save a new database connection
    - list: List saved connections
    - remove: Remove a specific saved connection
    - remove-all: Remove all saved connections

    Use 'peepdb COMMAND --help' for more information on a specific command.
    """
    pass

@cli.command()
@click.argument('connection_name')
@click.option('--table', help='Specific table to view')
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
@click.option('--page', type=int, default=1, help='Page number for pagination')
@click.option('--page-size', type=int, default=100, help='Number of rows per page')
def view(connection_name, table, format, page, page_size):
    """
    View database tables.

    CONNECTION_NAME is the name of the saved database connection to use.

    Examples:
    peepdb view mydb
    peepdb view mydb --table users --page 2 --page-size 50
    peepdb view mydb --format json
    """
    connection = get_connection(connection_name)
    if not connection:
        click.echo(f"Error: No saved connection found with name '{connection_name}'.")
        return

    db_type, host, user, password, database = connection
    result = peep_db(db_type, host, user, password, database, table, format=format, page=page, page_size=page_size)

    if format == 'table':
        click.echo(result)
        if table:
            click.echo("\nNavigation:")
            click.echo(f"Current Page: {page}")
            click.echo(f"Next Page: peepdb view {connection_name} --table {table} --page {page + 1} --page-size {page_size}")
            click.echo(f"Previous Page: peepdb view {connection_name} --table {table} --page {max(1, page - 1)} --page-size {page_size}")
    else:
        click.echo(json.dumps(result, indent=2, cls=CustomEncoder))

@cli.command()
@click.argument('connection_name')
@click.option('--db-type', type=click.Choice(['mysql', 'postgres', 'mariadb']), required=True, help='Database type')
@click.option('--host', required=True, help='Database host')
@click.option('--user', required=True, help='Database user')
@click.option('--password', required=True, prompt=True, hide_input=True, help='Database password')
@click.option('--database', required=True, help='Database name')
def save(connection_name, db_type, host, user, password, database):
    """
    Save a new database connection.

    CONNECTION_NAME is the name to give to this saved connection.

    Example:
    peepdb save mydb --db-type mysql --host localhost --user root --database myapp
    """
    save_connection(connection_name, db_type, host, user, password, database)
    click.echo(f"Connection '{connection_name}' saved successfully.")

@cli.command()
def list():
    """
    List saved connections.

    This command displays all the database connections you have saved.

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

    CONNECTION_NAME is the name of the saved connection to remove.

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

    This command will delete all your saved database connections.
    Use with caution.

    Example:
    peepdb remove-all
    """
    count = remove_all_connections()
    click.echo(f"{count} connection(s) have been removed.")

def main():
    cli()

if __name__ == '__main__':
    main()