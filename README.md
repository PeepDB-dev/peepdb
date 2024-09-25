# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, MariaDB, and SQLite, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, MariaDB, and SQLite.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface powered by Click.
- **Secure Local Storage**: Securely store database connection details with encryption on your local machine.
- **Lightweight**: Minimal footprint, designed for speed.
- **Formatted Output**: View data in a clean, formatted table or JSON format.
- **Pagination**: Efficiently handle large datasets by viewing data in manageable chunks.
- **SQLite Support**: Directly view SQLite database files without needing a server.

## 🎬 peepDB in Action

Here's a quick demonstration of peepDB:

![peepDB Demo](images/demo.gif)

## 🖼️ peepDB stills

![peepDB example 2](images/peepdb_example2.png)

> **Note:** The above image reflects the commands used in the official release (v0.1.3)

## 📦 Installation

You can install peepDB directly from PyPI:

```bash
pip install peepdb
```

**Requirements:**
- Python 3.9 or higher
- pip (Python package installer)

For detailed installation instructions, including system dependencies, please refer to our [Installation Guide](installation.md).

## 🛠️ Usage

peepDB uses a command-based structure for easier and more intuitive use. Here are the main commands with examples:

### 1. Save Your Database Connection Details

```bash
# For MySQL
peepdb save myapp_mysql --db-type mysql --host localhost --user root --database myapp

# For PostgreSQL
peepdb save analytics_pg --db-type postgres --host 192.168.1.100 --user admin --database analytics

# For MariaDB
peepdb save blog_mariadb --db-type mariadb --host blog.example.com --user bloguser --database wordpress

# For SQLite
peepdb save local_sqlite --db-type sqlite --database /path/to/mydb.sqlite
```

### 2. List Saved Connections

```bash
peepdb list
```

### 3. View Tables

View all tables:
```bash
peepdb view myapp_mysql
```

View a specific table:
```bash
peepdb view analytics_pg --table user_metrics
```

### 4. Pagination

Use pagination to handle large datasets:
```bash
peepdb view blog_mariadb --table posts --page 2 --page-size 50
```

### 5. Choose Output Format

Get output in JSON format:
```bash
peepdb view local_sqlite --table products --format json
```

### 6. Remove Saved Connections

Remove a specific connection:
```bash
peepdb remove myapp_mysql
```

Remove all connections:
```bash
peepdb remove-all
```

For more detailed usage information and examples, please refer to our [Usage Guide](usage.md).

## 👨‍💻 For Developers

Please refer to our [Contributing Guide](CONTRIBUTING.md) for information on setting up the development environment, running tests, and contributing to peepDB.

## 🔒 Security

peepDB implements several security measures to protect your database connection details:

1. **Local Storage**: All connection details are stored locally on your machine, not on any remote servers.
2. **Encryption**: Connection details are encrypted before being stored, using the cryptography library.
3. **Secure Password Input**: Passwords are never shown in plain text and are input securely.
4. **Keyring Support**: Optionally use your system's keyring for storing encryption keys.

However, please note that while we strive to implement best security practices, peepDB's security has not been verified by a third party. Users should exercise caution and follow general security best practices when using any tool that handles sensitive information.

## 📜 License

Distributed under the GNU General Public License Version 3. See the [LICENSE](LICENSE) file for more details.

## 📚 Documentation

For more detailed documentation, please visit our [GitHub Pages](https://peepdb.dev/).
