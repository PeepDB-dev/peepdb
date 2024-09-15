---
title: Home
layout: home
---

# peepDB

**peepDB** is an open-source command-line tool and Python library designed for developers and database administrators who need a fast and efficient way to inspect their database tables without writing SQL queries. With support for MySQL, PostgreSQL, and MariaDB, peepDB is lightweight, secure, and incredibly easy to use.

## 🚀 Features

- **Multi-Database Support**: Works with MySQL, PostgreSQL, and MariaDB.
- **Quick Data Inspection**: View all tables or a specific table with a simple command.
- **User-Friendly CLI**: Easy-to-use command-line interface powered by Click.
- **Secure Local Storage**: Securely store database connection details with encryption on your local machine.
- **Lightweight**: Minimal footprint, designed for speed.
- **Formatted Output**: View data in a clean, formatted table or JSON format.
- **Pagination**: Efficiently handle large datasets by viewing data in manageable chunks.

## Getting Started

To get started with peepDB, check out the following pages:

- [Installation](installation.html): Learn how to install peepDB.
- [Usage](usage.html): Discover how to use peepDB effectively.
- [Contributing](contributing.html): Find out how you can contribute to the project.

## 🔒 Security

peepDB implements several security measures to protect your database connection details:

1. **Local Storage**: All connection details are stored locally on your machine, not on any remote servers.
2. **Encryption**: Connection details are encrypted before being stored, using the cryptography library.
3. **Secure Password Input**: Passwords are never shown in plain text and are input securely.

However, please note that while we strive to implement best security practices, peepDB's security has not been verified by a third party. Users should exercise caution and follow general security best practices when using any tool that handles sensitive information.

The encryption key is stored in your user directory (~/.peepdb/key.key). Keep this key safe and do not share it.

## 📜 License

peepDB is distributed under the GNU General Public License Version 3. See the [LICENSE](https://github.com/evangelosmeklis/peepdb/blob/main/LICENSE) file for more details.
