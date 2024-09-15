---
title: Usage
layout: default
---

# 🛠️ Usage

peepDB provides a user-friendly command-line interface for interacting with your databases. Here are the main commands and their usage:

## Saving Database Connection Details

You can securely store your connection details for easier access:

```bash
peepdb save <connection_name> --db-type [mysql/postgres/mariadb] --host <host> --user <user> --database <database>
```

You'll be prompted securely for the password.

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

## Pagination

Use pagination to handle large datasets:

```bash
peepdb view <connection_name> --table <table_name> --page <page_number> --page-size <rows_per_page>
```

## Choosing Output Format

By default, peepDB displays data in a formatted table. You can also get the output in JSON format:

```bash
peepdb view <connection_name> --format json
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

> **Note:** Both of these commands will ask for confirmation before proceeding with the removal.

## Help

For more detailed usage information on any command, use the `--help` option:

```bash
peepdb <command> --help
```

## Examples

Here are some example commands to help you get started:

1. Save MySQL connection details:
   ```bash
   peepdb save myapp_db --db-type mysql --host localhost --user root --database myapp
   ```

2. View all tables in the saved MySQL database:
   ```bash
   peepdb view myapp_db
   ```

3. View a specific table with pagination:
   ```bash
   peepdb view myapp_db --table users --page 1 --page-size 50
   ```

4. Get output in JSON format:
   ```bash
   peepdb view myapp_db --format json
   ```

5. Remove a saved connection:
   ```bash
   peepdb remove myapp_db
   ```

Remember to use the `--help` option with any command for more detailed information on its usage and options.
