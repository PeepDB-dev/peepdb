
# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, and MariaDB, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, and MariaDB.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface.
- **Secure Storage**: Securely store database connection details with encryption.
- **Lightweight**: Minimal footprint, designed for speed.

> **Note:** Currently, peepDB supports one connection per database type (e.g., one MySQL, one PostgreSQL, one MariaDB) concurrently.

## 📦 Installation

To install peepDB, simply use pip:

```bash
pip install peepDB
```

## 🛠️ Usage

### Command-Line Interface

#### 1. Save Your Database Connection Details (Optional)

You can securely store your connection details for easier access:

```bash
peepDB <db_type> --host <host> --user <user> --password <password> --database <database> --save
```

#### 2. View All Tables or a Specific Table

To view all tables in the database:

```bash
peepDB <db_type>
```

To view a specific table:

```bash
peepDB <db_type> --table <table_name>
```

### Examples

- **Save MySQL connection details:**

  ```bash
  peepDB mysql --host localhost --user root --password mypassword --database mydb --save
  ```

- **View all tables in the saved MySQL database:**

  ```bash
  peepDB mysql
  ```

- **View a specific table:**

  ```bash
  peepDB mysql --table users
  ```

- **Use PostgreSQL without saving details:**

  ```bash
  peepDB postgres --host localhost --user postgres --password mypassword --database mydb --table customers
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
