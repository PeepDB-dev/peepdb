import pytest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import sys
import os
import json
from peepdb.cli import main
from peepdb.config import remove_all_connections, CONFIG_FILE

@pytest.fixture
def mock_stdin(monkeypatch):
    def mock_input(prompt):
        return "mocked_input"
    monkeypatch.setattr('builtins.input', mock_input)

@pytest.fixture
def mock_stdout():
    return StringIO()

@patch('peepdb.cli.save_connection')
def test_save_connection(mock_save, mock_stdin, mock_stdout):
    test_args = ['peepdb', 'test_db', '--save', '--db-type', 'mysql', '--host', 'localhost', 
                 '--user', 'testuser', '--password', 'testpass', '--database', 'testdb']
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_save.assert_called_once_with('test_db', 'mysql', 'localhost', 'testuser', 'testpass', 'testdb')
    assert "Connection 'test_db' saved successfully." in mock_stdout.getvalue()

@patch('peepdb.cli.list_connections')
def test_list_connections(mock_list, mock_stdout):
    test_args = ['peepdb', '--list']
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_list.assert_called_once()

@patch('peepdb.cli.remove_connection')
@patch('peepdb.cli.confirm_action')
def test_remove_connection(mock_confirm, mock_remove, mock_stdout):
    test_args = ['peepdb', '--remove', 'test_db']
    mock_confirm.return_value = True
    mock_remove.return_value = True
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_confirm.assert_called_once()
    mock_remove.assert_called_once_with('test_db')
    assert "Connection 'test_db' has been removed." in mock_stdout.getvalue()

@patch('peepdb.config.os.path.exists')
@patch('peepdb.config.os.remove')
def test_remove_all_connections(mock_remove, mock_exists):
    # Test when file exists and is valid
    mock_exists.return_value = True
    mock_file = mock_open(read_data='{"conn1": {}, "conn2": {}}')
    with patch('builtins.open', mock_file):
        count = remove_all_connections()
    assert count == 2
    mock_remove.assert_called_once_with(CONFIG_FILE)

    # Reset mock_remove for the next test
    mock_remove.reset_mock()

    # Test when file doesn't exist
    mock_exists.return_value = False
    count = remove_all_connections()
    assert count == 0
    mock_remove.assert_not_called()

    # Test when file is deleted between check and remove
    mock_exists.return_value = True
    mock_remove.side_effect = FileNotFoundError
    mock_file = mock_open(read_data='{"conn1": {}, "conn2": {}}')
    with patch('builtins.open', mock_file):
        count = remove_all_connections()
    assert count == 2
    mock_remove.assert_called_with(CONFIG_FILE)

    # Reset mock_remove for the next test
    mock_remove.reset_mock()
    mock_remove.side_effect = None

    # Test when file exists but is not valid JSON
    mock_exists.return_value = True
    mock_file = mock_open(read_data='invalid json')
    with patch('builtins.open', mock_file):
        count = remove_all_connections()
    assert count == 0
    mock_remove.assert_called_with(CONFIG_FILE)

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_peep_db_table_format(mock_get_connection, mock_peep_db, mock_stdout):
    test_args = ['peepdb', 'test_db']
    mock_get_connection.return_value = ('mysql', 'localhost', 'testuser', 'testpass', 'testdb')
    mock_peep_db.return_value = """Table: users
+----+------+-------+
| id | name | email |
+====+======+=======+
|  1 | John | j@e.c |
+----+------+-------+
|  2 | Jane | j@e.c |
+----+------+-------+

Table: orders
+----+------+-------+
| id | user | total |
+====+======+=======+
|  1 |    1 |   100 |
+----+------+-------+
|  2 |    2 |   200 |
+----+------+-------+"""

    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_get_connection.assert_called_once_with('test_db')
    mock_peep_db.assert_called_once_with('mysql', 'localhost', 'testuser', 'testpass', 'testdb', None, format='table')
    
    expected_output = """Table: users
+----+------+-------+
| id | name | email |
+====+======+=======+
|  1 | John | j@e.c |
+----+------+-------+
|  2 | Jane | j@e.c |
+----+------+-------+

Table: orders
+----+------+-------+
| id | user | total |
+====+======+=======+
|  1 |    1 |   100 |
+----+------+-------+
|  2 |    2 |   200 |
+----+------+-------+
"""
    assert mock_stdout.getvalue().strip() == expected_output.strip()

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_peep_db_json_format(mock_get_connection, mock_peep_db, mock_stdout):
    test_args = ['peepdb', 'test_db', '--format', 'json']
    mock_get_connection.return_value = ('mysql', 'localhost', 'testuser', 'testpass', 'testdb')
    mock_peep_db.return_value = {
        'users': [{'id': 1, 'name': 'John', 'email': 'j@e.c'}, {'id': 2, 'name': 'Jane', 'email': 'j@e.c'}],
        'orders': [{'id': 1, 'user': 1, 'total': 100}, {'id': 2, 'user': 2, 'total': 200}]
    }

    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_get_connection.assert_called_once_with('test_db')
    mock_peep_db.assert_called_once_with('mysql', 'localhost', 'testuser', 'testpass', 'testdb', None, format='json')
    
    expected_output = """{
  "users": [
    {
      "id": 1,
      "name": "John",
      "email": "j@e.c"
    },
    {
      "id": 2,
      "name": "Jane",
      "email": "j@e.c"
    }
  ],
  "orders": [
    {
      "id": 1,
      "user": 1,
      "total": 100
    },
    {
      "id": 2,
      "user": 2,
      "total": 200
    }
  ]
}"""
    assert mock_stdout.getvalue().strip() == expected_output.strip()

if __name__ == '__main__':
    pytest.main()