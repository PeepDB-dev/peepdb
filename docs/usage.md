---
title: Usage
layout: default
---

# 🛠️ Usage

peepDB provides a user-friendly command-line interface for interacting with your databases. Here are the main commands and their usage with examples:

## Saving Database Connection Details

You can securely store your connection details for easier access:

```bash
peepdb save <connection_name> --db-type [mysql/postgres/mariadb/sqlite] --host <host> --user <user> --database <database>
```

You'll be prompted securely for the password (except for SQLite).

Examples:

```bash
# MySQL
peepdb save myapp_mysql --db-type mysql --host localhost --user root --database myapp

# PostgreSQL
peepdb save analytics_pg --db-type postgres --host 192.168.1.100 --user admin --database analytics

# MariaDB
peepdb save blog_mariadb --db-type mariadb --host blog.example.com --user bloguser --database wordpress

# SQLite
peepdb save local_sqlite --db-type sqlite --database /path/to/mydb.sqlite
```

## Listing Saved Connections

To view all saved database connections:

```bash
peepdb list
```

## Viewing Tables

To view all tables in the database:

```bash
peepdb view <connection_name>
```

To view a specific table:

```bash
peepdb view <connection_name> --table <table_name>
```

Examples:

```bash
# View all tables in a MySQL database
peepdb view myapp_mysql

# View a specific table in a PostgreSQL database
peepdb view analytics_pg --table user_metrics

# View a table in a SQLite database
peepdb view local_sqlite --table products
```

## Pagination

Use pagination to handle large datasets:

```bash
peepdb view <connection_name> --table <table_name> --page <page_number> --page-size <rows_per_page>
```

Example:

```bash
# View the second page of the 'posts' table, with 50 rows per page
peepdb view blog_mariadb --table posts --page 2 --page-size 50
```

## Choosing Output Format

By default, peepDB displays data in a formatted table. You can also get the output in JSON format:

```bash
peepdb view <connection_name> --format json
```

Example:

```bash
# Get JSON output for the 'products' table in a SQLite database
peepdb view local_sqlite --table products --format json
```

## Removing Saved Connections

To remove a specific saved connection:

```bash
peepdb remove <connection_name>
```

To remove all saved connections:

```bash
peepdb remove-all
```

Examples:

```bash
# Remove a specific connection
peepdb remove myapp_mysql

# Remove all connections
peepdb remove-all
```

> **Note:** Both of these commands will ask for confirmation before proceeding with the removal.

## Help

For more detailed usage information on any command, use the `--help` option:

```bash
peepdb <command> --help
```

Example:

```bash
peepdb view --help
```

Remember to use the `--help` option with any command for more detailed information on its usage and options.
