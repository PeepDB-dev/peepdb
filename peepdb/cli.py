import argparse
import json
from .core import peep_db
from .config import get_connection, save_connection, list_connections
from decimal import Decimal
from datetime import date

def main():
    parser = argparse.ArgumentParser(description="Quick database table viewer")
    parser.add_argument("db_type", choices=["mysql", "postgres", "mariadb"], help="Database type")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--user", help="Database user")
    parser.add_argument("--password", help="Database password")
    parser.add_argument("--database", help="Database name")
    parser.add_argument("--table", help="Specific table to view (optional)")
    parser.add_argument("--save", action="store_true", help="Save connection details")
    parser.add_argument("--list", action="store_true", help="List saved connections")
    args = parser.parse_args()

    if args.list:
        list_connections()
        return
    
    if args.save:
        save_connection(args.db_type, args.host, args.user, args.password, args.database)
        print("Connection details saved.")
        return

    connection = get_connection(args.db_type)
    if connection:
        host, user, password, database = connection
    else:
        host, user, password, database = args.host, args.user, args.password, args.database

    result = peep_db(args.db_type, host, user, password, database, args.table)

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