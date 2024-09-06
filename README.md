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

Currently, peepDB is not available on PyPI. To install it, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/evangelosmeklis/peepDB.git
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

#### 4. Choose Output Format

By default, peepDB displays data in a formatted table. You can also get the output in JSON format:

```bash
peepDB <connection_name> --format json
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
   peepDB myapp_db
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
   peepDB myapp_db --table users
   ```

4. **Get output in JSON format:**

   ```bash
   peepDB myapp_db --format json
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
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📜 License

Distributed under the GNU General Public License Version 3. See the `LICENSE` file for more details.