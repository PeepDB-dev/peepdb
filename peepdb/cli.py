import argparse
import json
from .core import peep_db
from .config import get_connection, save_connection, list_connections
from decimal import Decimal
from datetime import date

def prompt_for_input(prompt, is_password=False):
    if is_password:
        import getpass
        return getpass.getpass(prompt)
    else:
        return input(prompt)

def main():
    parser = argparse.ArgumentParser(description="Quick database table viewer")
    
    parser.add_argument("database_name", nargs='?', help="Name of the saved database connection")
    parser.add_argument("--save", action="store_true", help="Save a new connection")
    parser.add_argument("--list", action="store_true", help="List saved connections")
    parser.add_argument("--table", help="Specific table to view (optional)")
    
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
    result = peep_db(db_type, host, user, password, database, args.table)

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, date):
                return obj.isoformat()
            return super(CustomEncoder, self).default(obj)
    
    print(json.dumps(result, indent=2, cls=CustomEncoder))

if __name__ == "__main__":
    main()