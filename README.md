# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, and MariaDB, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, and MariaDB.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface.
- **Secure Storage**: Securely store database connection details with encryption.
- **Lightweight**: Minimal footprint, designed for speed.
- **Formatted Output**: View data in a clean, formatted table or JSON format.

## 📢 Upcoming Changes (In Development)

We're working on some exciting updates to peepDB! Here's what's coming in the next version:

- Switching from argparse to Click for an improved CLI experience
- New command structure for easier and more intuitive use
- Enhanced help messages and documentation

These changes are currently in development and not yet released. Stay tuned for the upcoming version!

> Note: The current release still uses the argparse-based CLI. The information below reflects the current stable version.

## 📦 Installation

You can install peepDB directly from PyPI:

```bash
pip install peepdb
```

**Requirements:**
- Python 3.6 or higher
- pip (Python package installer)

> **Note:** If peepdb gives an error like "The term 'peepdb' is not recognized as the name of a cmdlet" remember to add the Python Scripts folder to your PATH in Windows.

## System Dependencies

Before installing peepdb, ensure you have the following system dependencies:

```bash
sudo apt-get update
sudo apt-get install libmariadb3 libmariadb-dev
```

Verify the installation by running:
```bash
peepdb --version
```

## 🛠️ Current Usage (Stable Version)

### 1. Save Your Database Connection Details (Optional)

```bash
peepdb <connection_name> --save --db-type [mysql/postgres/mariadb] --host <host> --user <user> --password <password> --database <database>
```

### 2. List Saved Connections

```bash
peepdb --list
```

### 3. View All Tables or a Specific Table

View all tables:
```bash
peepdb <connection_name>
```

View a specific table:
```bash
peepdb <connection_name> --table <table_name>
```

### 4. Choose Output Format

Get output in JSON format:
```bash
peepdb <connection_name> --format json
```

### 5. Remove Saved Connections

Remove a specific connection:
```bash
peepdb --remove <connection_name>
```

Remove all connections:
```bash
peepdb --remove-all
```

For more detailed usage information, run:
```bash
peepdb --help
```

## 👨‍💻 For Developers

Please refer to our [Contributing Guide](CONTRIBUTING.md) for information on setting up the development environment, running tests, and contributing to peepDB.

## 🔒 Security

peepDB uses encryption to securely store database connection details. The encryption key is stored in your user directory (~/.peepdb/key.key). Keep this key safe and do not share it.

## 📜 License

Distributed under the GNU General Public License Version 3. See the [LICENSE](LICENSE) file for more details.

## 📚 Documentation

For more detailed documentation, please visit our [GitHub Pages](https://peepdb.dev/).
