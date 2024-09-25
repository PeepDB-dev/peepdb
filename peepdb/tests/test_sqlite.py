import unittest
import sqlite3
import tempfile
import os
import json
from peepdb.core import peep_db

class TestPeepDBSQLite(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create a test table and insert some data
        self.cursor.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        self.cursor.executemany(
            'INSERT INTO test_table (name, age) VALUES (?, ?)',
            [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
        )
        self.conn.commit()

    def tearDown(self):
        # Close the connection and remove the temporary database
        self.conn.close()
        import time
        time.sleep(0.1)  # Give a small delay to ensure all file handles are released
        try:
            os.unlink(self.db_path)
        except PermissionError:
            print(f"Warning: Unable to delete temporary file: {self.db_path}")

    def test_peep_db_sqlite(self):
        # Test peep_db function with SQLite
        result = peep_db('sqlite', database=self.db_path, table='test_table', format='json')

        # Parse the JSON result
        data = json.loads(result)

        # Check if the correct table is returned
        self.assertIn('test_table', data)

        # Check if the correct number of rows are returned
        self.assertEqual(len(data['test_table']['data']), 3)

        # Check if the data is correct
        expected_data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        self.assertEqual(data['test_table']['data'], expected_data)

    def test_peep_db_sqlite_table_list(self):
        # Test peep_db function with SQLite to list tables
        result = peep_db('sqlite', database=self.db_path)
        
        # The result should be a string containing 'test_table'
        self.assertIn('test_table', result)

if __name__ == '__main__':
    unittest.main()