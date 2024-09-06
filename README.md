# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, and MariaDB, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, and MariaDB.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface.
- **Secure Storage**: Securely store database connection details with encryption.
- **Lightweight**: Minimal footprint, designed for speed.
- **Formatted Output**: View data in a clean, formatted table or JSON format.

## 📦 Installation

You can install peepDB directly from PyPI:

```bash
pip install peepdb
```

## 🛠️ Usage

### Command-Line Interface

#### 1. Save Your Database Connection Details (Optional)

You can securely store your connection details for easier access:

```bash
peepdb <connection_name> --save --db-type [mysql/postgres/mariadb] --host <host> --user <user> --password <password> --database <database>
```

#### 2. List Saved Connections

To view all saved database connections:

```bash
peepdb --list
```

#### 3. View All Tables or a Specific Table

To view all tables in the database:

```bash
peepdb <connection_name>
```

To view a specific table:

```bash
peepdb <connection_name> --table <table_name>
```

#### 4. Choose Output Format

By default, peepDB displays data in a formatted table. You can also get the output in JSON format:

```bash
peepdb <connection_name> --format json
```

#### 5. Remove Saved Connections

To remove a specific saved connection:

```bash
peepdb --remove <connection_name>
```

To remove all saved connections:

```bash
peepdb --remove-all
```

> **Note:** Both of these commands will ask for confirmation before proceeding with the removal.

### Examples

1. **Save MySQL connection details:**

   ```bash
   peepdb myapp_db --save --db-type mysql --host localhost --user root --password mypassword --database myapp
   ```

2. **View all tables in the saved MySQL database:**

   ```bash
   peepdb myapp_db
   ```

   Output:
   ```
   Table: users
   +----+----------+----------------------+
   | id | username | email                |
   +====+==========+======================+
   |  1 | john_doe | john.doe@example.com |
   +----+----------+----------------------+
   |  2 | jane_doe | jane.doe@example.com |
   +----+----------+----------------------+

   Table: orders
   +----+---------+------------+--------+
   | id | user_id | order_date | total  |
   +====+=========+============+========+
   |  1 |       1 | 2023-05-01 | 100.00 |
   +----+---------+------------+--------+
   |  2 |       2 | 2023-05-02 | 150.50 |
   +----+---------+------------+--------+
   ```

3. **View a specific table:**

   ```bash
   peepdb myapp_db --table users
   ```

4. **Get output in JSON format:**

   ```bash
   peepdb myapp_db --format json
   ```

   Output:
   ```json
   {
     "users": [
       {"id": 1, "username": "john_doe", "email": "john.doe@example.com"},
       {"id": 2, "username": "jane_doe", "email": "jane.doe@example.com"}
     ],
     "orders": [
       {"id": 1, "user_id": 1, "order_date": "2023-05-01", "total": 100.00},
       {"id": 2, "user_id": 2, "order_date": "2023-05-02", "total": 150.50}
     ]
   }
   ```

5. **Use PostgreSQL without saving details:**

   ```bash
   peepdb analytics_db --save --db-type postgres --host localhost --user postgres --password mypassword --database analytics
   ```

## 🔒 Security

peepDB uses encryption to securely store your database connection details. The encryption key is stored in your user directory (~/.peepdb/key.key). Make sure to keep this key safe and do not share it.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to Contribute:

1. Fork the repository.
2. Create your feature branch ([`git checkout -b feature/AmazingFeature`](command:_github.copilot.openSymbolFromReferences?%5B%22git%20checkout%20-b%20feature%2FAmazingFeature%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22c%3A%5C%5CUsers%5C%5CVangelis%5C%5CDesktop%5C%5CpeepDB%5C%5CREADME.md%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fc%253A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A172%2C%22character%22%3A36%7D%7D%5D%5D "Go to definition")).
3. Commit your changes ([`git commit -m 'Add some AmazingFeature'`](command:_github.copilot.openSymbolFromReferences?%5B%22git%20commit%20-m%20'Add%20some%20AmazingFeature'%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22c%3A%5C%5CUsers%5C%5CVangelis%5C%5CDesktop%5C%5CpeepDB%5C%5CREADME.md%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fc%253A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A173%2C%22character%22%3A29%7D%7D%5D%5D "Go to definition")).
4. Push to the branch ([`git push origin feature/AmazingFeature`](command:_github.copilot.openSymbolFromReferences?%5B%22git%20push%20origin%20feature%2FAmazingFeature%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22c%3A%5C%5CUsers%5C%5CVangelis%5C%5CDesktop%5C%5CpeepDB%5C%5CREADME.md%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fc%253A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FREADME.md%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A172%2C%22character%22%3A15%7D%7D%5D%5D "Go to definition")).
5. Open a Pull Request.

## 📜 License

Distributed under the GNU General Public License Version 3. See the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FVangelis%2FDesktop%2FpeepDB%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Vangelis\Desktop\peepDB\LICENSE") file for more details.