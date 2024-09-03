import argparse
import json
from .core import peep_db
from .config import get_connection, save_connection, list_connections, remove_connection, remove_all_connections
from decimal import Decimal
from datetime import date

def prompt_for_input(prompt, is_password=False):
    if is_password:
        import getpass
        return getpass.getpass(prompt)
    else:
        return input(prompt)

def confirm_action(prompt):
    while True:
        response = input(f"{prompt} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please answer with 'y' or 'n'.")

def main():
    parser = argparse.ArgumentParser(description="Quick database table viewer")
    
    parser.add_argument("database_name", nargs='?', help="Name of the saved database connection")
    parser.add_argument("--save", action="store_true", help="Save a new connection")
    parser.add_argument("--list", action="store_true", help="List saved connections")
    parser.add_argument("--remove", metavar="CONNECTION_NAME", help="Remove a specific saved connection")
    parser.add_argument("--remove-all", action="store_true", help="Remove all saved connections")
    parser.add_argument("--table", help="Specific table to view (optional)")
    parser.add_argument("--format", choices=['table', 'json'], default='table', help="Output format (default: table)")

    # Arguments for saving a new connection
    parser.add_argument("--db-type", choices=["mysql", "postgres", "mariadb"], help="Database type")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--user", help="Database user")
    parser.add_argument("--password", help="Database password")
    parser.add_argument("--database", help="Database name")
    
    args = parser.parse_args()

    if args.list:
        list_connections()
        return

    if args.remove:
        if confirm_action(f"Are you sure you want to remove the connection '{args.remove}'?"):
            if remove_connection(args.remove):
                print(f"Connection '{args.remove}' has been removed.")
            else:
                print(f"No connection named '{args.remove}' found.")
        else:
            print("Operation cancelled.")
        return

    if args.remove_all:
        if confirm_action("Are you sure you want to remove ALL saved connections? This action cannot be undone."):
            count = remove_all_connections()
            print(f"{count} connection(s) have been removed.")
        else:
            print("Operation cancelled.")
        return
    
    if args.save:
        # Prompt for database name if not provided
        db_name = args.database_name or prompt_for_input("Enter a name for this database connection: ")
        
        # Prompt for other details if not provided
        db_type = args.db_type or prompt_for_input("Enter database type (mysql/postgres/mariadb): ")
        host = args.host or prompt_for_input("Enter database host: ")
        user = args.user or prompt_for_input("Enter database user: ")
        password = args.password or prompt_for_input("Enter database password: ", is_password=True)
        database = args.database or prompt_for_input("Enter database name: ")

        save_connection(db_name, db_type, host, user, password, database)
        print(f"Connection '{db_name}' saved successfully.")
        return

    if not args.database_name:
        print("Error: Database name is required unless using --list or --save.")
        return

    connection = get_connection(args.database_name)
    if not connection:
        print(f"Error: No saved connection found with name '{args.database_name}'. Use --save to create a new connection.")
        return

    db_type, host, user, password, database = connection
    
    result = peep_db(db_type, host, user, password, database, args.table, format=args.format)

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, date):
                return obj.isoformat()
            return super(CustomEncoder, self).default(obj)
    
    if args.format == 'table':
        print(result)
    else:
        print(json.dumps(result, indent=2, cls=CustomEncoder))

if __name__ == "__main__":
    main()