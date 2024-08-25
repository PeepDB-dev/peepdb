
# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, and MariaDB, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, and MariaDB.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface.
- **Secure Storage**: Securely store database connection details with encryption.
- **Lightweight**: Minimal footprint, designed for speed.

## 📦 Installation

Currently, peepDB is not available on PyPI. To install it, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/evangelosmeklis/peepDB.git
```
```bash
cd peepDB
```

2. Install the package in editable mode:

> **Note:** Create a virtual environment before running this command

```bash 
pip install -e .
 ```

3. Run peepDB:

```bash 
peepdb [command] 
 ```
See Usage for more info on commands

> **Note:**  We're working on making peepDB available via pip for easier installation in the future.

## 🛠️ Usage

### Command-Line Interface

#### 1. Save Your Database Connection Details (Optional)

You can securely store your connection details for easier access:

```bash
peepdb <connection_name> --save --db-type [mysql/postgres/mariadb] --host <host> --user <user> --password <password> --database <database>
```

#### 2.  List Saved Connections

To view all saved database connections:

```bash
peepDB --list
```

#### 3. View All Tables or a Specific Table

To view all tables in the database:

```bash
peepDB <connection_name>
```

To view a specific table:

```bash
peepDB <connection_name> --table <table_name>
```

#### 4.  Removed Saved Connections

To remove a specific saved connection:

```bash
peepdb --remove <connection_name>
```
To remove all saved connection:

```bash
peepdb --remove-all
```
> **Note:** Both of these commands will ask for confirmation before proceeding with the removal.

### Examples

- **Save MySQL connection details:**

  ```bash
  peepdb myapp_db --save --db-type mysql --host localhost --user root --password mypassword --database myapp
  ```

- **View all tables in the saved MySQL database:**

  ```bash
  peepDB myapp_db
  ```

- **View a specific table:**

  ```bash
  peepDB myapp_db --table users
  ```

- **Use PostgreSQL without saving details:**

  ```bash
  peepdb analytics_db --save --db-type postgres --host localhost --user postgres --password mypassword --database analytics
  ```

### Python Library (Coming Soon)

You will also be able to use peepDB in your Python scripts:

```python
from peepdb.core import peep_db
```

## 🔒 Security

peepDB uses encryption to securely store your database connection details. The encryption key is stored in your user directory (~/.peepdb/key.key). Make sure to keep this key safe and do not share it.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to Contribute:

1. Fork the repository.
2. Create your feature branch (\`git checkout -b feature/AmazingFeature\`).
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`).
4. Push to the branch (\`git push origin feature/AmazingFeature\`).
5. Open a Pull Request.

## 📜 License

Distributed under the GNU General Public License Version 3. See the \`LICENSE\` file for more details.
