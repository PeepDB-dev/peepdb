# peepDB

peepDB is an Open Source command-line tool and Python library that allows you to quickly view the contents of MySQL, PostgreSQL, or MariaDB database tables. It's designed for developers and database administrators who need a fast way to inspect their data without writing SQL queries.

## Features

- Support for MySQL, PostgreSQL, and MariaDB
- View all tables in a database or a specific table
- Simple command-line interface
- Secure storage of database connection details
- Fast and lightweight

Currently it supports one MySQL database connection concurrently with PostgreSQL and MariaDB 
but not multiple connections of the same db type

## Installation

You can install peepDB using pip: (not yet)

pip install peepDB 

## Usage

### Command Line Interface

To use peepDB from the command line:

1. Save your database connection details (optional):

peepDB <db_type> --host <host> --user <user> --password <password> --database <database> --save

2. View a specific table or all tables:

peepDB <db_type> [--table <table_name>]

### Save MySQL connection details
peepDB mysql --host localhost --user root --password mypassword --database mydb --save

### View all tables in the saved MySQL database
peepDB mysql

### View a specific table
peepDB mysql --table users

### Use PostgreSQL without saving details
peepDB postgres --host localhost --user postgres --password mypassword --database mydb --table customers

### Python Library

You can also use peepDB in your Python scripts:

from peepdb.core import peep_db

# View all tables
result = peep_db('mysql', 'localhost', 'root', 'mypassword', 'mydb')

# View a specific table
result = peep_db('mysql', 'localhost', 'root', 'mypassword', 'mydb', table='users')

print(result)

## Security
peepDB uses encryption to securely store your database connection details. The encryption key is stored in your user directory (~/.peepdb/key.key). Make sure to keep this key safe and do not share it.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

## License
Distributed under the MIT License. See LICENSE for more information.