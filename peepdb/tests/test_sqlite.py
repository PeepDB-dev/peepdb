import unittest
import os
import sqlite3
from peepdb.db.sqlite import SQLiteDatabase

class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database for testing
        self.db_path = 'test_sqlite.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create test tables and insert some data
        self.cursor.execute('''CREATE TABLE users
                             (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
        self.cursor.execute('''CREATE TABLE products
                             (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
        self.cursor.executemany('INSERT INTO users VALUES (?, ?, ?)',
                                [(1, 'Alice', 'alice@test.com'),
                                 (2, 'Bob', 'bob@test.com')])
        self.cursor.executemany('INSERT INTO products VALUES (?, ?, ?)',
                                [(1, 'Widget', 9.99),
                                 (2, 'Gadget', 19.99)])
        self.conn.commit()
        
        # Initialize the SQLiteDatabase instance
        self.db = SQLiteDatabase(self.db_path, '', '', '')
        self.db.connect()

    def tearDown(self):
        # Clean up: close connections and remove the test database
        self.db.disconnect()
        self.conn.close()
        os.remove(self.db_path)

    def test_fetch_tables(self):
        tables = self.db.fetch_tables()
        self.assertEqual(set(tables), {'users', 'products'})

    def test_fetch_data_users(self):
        result = self.db.fetch_data('users')
        self.assertEqual(result['total_rows'], 2)
        self.assertEqual(len(result['data']), 2)
        self.assertEqual(result['data'][0]['name'], 'Alice')
        self.assertEqual(result['data'][1]['email'], 'bob@test.com')

    def test_fetch_data_products(self):
        result = self.db.fetch_data('products')
        self.assertEqual(result['total_rows'], 2)
        self.assertEqual(len(result['data']), 2)
        self.assertEqual(result['data'][0]['name'], 'Widget')
        self.assertEqual(result['data'][1]['price'], 19.99)

    def test_fetch_data_pagination(self):
        result = self.db.fetch_data('users', page=1, page_size=1)
        self.assertEqual(result['total_rows'], 2)
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['name'], 'Alice')
        self.assertEqual(result['page'], 1)
        self.assertEqual(result['total_pages'], 2)

        result = self.db.fetch_data('users', page=2, page_size=1)
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['name'], 'Bob')
        self.assertEqual(result['page'], 2)

    def test_fetch_data_nonexistent_table(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.fetch_data('nonexistent_table')

if __name__ == '__main__':
    unittest.main()