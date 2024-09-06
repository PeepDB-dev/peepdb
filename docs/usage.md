---
title: Usage
layout: default
---

# Usage

peepDB provides a user-friendly command-line interface for interacting with your databases. Here are the main commands and their usage:

## Saving Database Connection Details

You can securely store your connection details for easier access:

```bash
peepdb <connection_name> --save --db-type [mysql/postgres/mariadb] --host <host> --user <user> --password <password> --database <database>
```

## Listing Saved Connections

To view all saved database connections:

```bash
peepdb --list
```

## Viewing Tables

To view all tables in the database:

```bash
peepdb <connection_name>
```

To view a specific table:

```bash
peepdb <connection_name> --table <table_name>
```

## Choosing Output Format

By default, peepDB displays data in a formatted table. You can also get the output in JSON format:

```bash
peepdb <connection_name> --format json
```

## Removing Saved Connections

To remove a specific saved connection:

```bash
peepdb --remove <connection_name>
```

To remove all saved connections:

```bash
peepdb --remove-all
```

> **Note:** Both of these commands will ask for confirmation before proceeding with the removal.

## Examples

Here are some example commands to help you get started:

1. Save MySQL connection details:
   ```bash
   peepdb myapp_db --save --db-type mysql --host localhost --user root --password mypassword --database myapp
   ```

2. View all tables in the saved MySQL database:
   ```bash
   peepdb myapp_db
   ```

3. View a specific table:
   ```bash
   peepdb myapp_db --table users
   ```

4. Get output in JSON format:
   ```bash
   peepdb myapp_db --format json
   ```

5. Use PostgreSQL without saving details:
   ```bash
   peepdb --db-type postgres --host localhost --user postgres --password mypassword --database analytics
   ```

For more detailed information on each command and its options, you can use the built-in help:

```bash
peepdb --help
```
