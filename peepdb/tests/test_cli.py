import pytest
from unittest.mock import patch, MagicMock
from peepdb.cli import main
from io import StringIO
import sys

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

@patch('peepdb.cli.remove_all_connections')
@patch('peepdb.cli.confirm_action')
def test_remove_all_connections(mock_confirm, mock_remove_all, mock_stdout):
    test_args = ['peepdb', '--remove-all']
    mock_confirm.return_value = True
    mock_remove_all.return_value = 2
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_confirm.assert_called_once()
    mock_remove_all.assert_called_once()
    assert "2 connection(s) have been removed." in mock_stdout.getvalue()

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_peep_db(mock_get_connection, mock_peep_db, mock_stdout):
    test_args = ['peepdb', 'test_db', '--table', 'users']
    mock_get_connection.return_value = ('mysql', 'localhost', 'testuser', 'testpass', 'testdb')
    mock_peep_db.return_value = {'users': [{'id': 1, 'name': 'Test User'}]}
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdout', mock_stdout):
            main()
    
    mock_get_connection.assert_called_once_with('test_db')
    mock_peep_db.assert_called_once_with('mysql', 'localhost', 'testuser', 'testpass', 'testdb', 'users')
    assert '"id": 1' in mock_stdout.getvalue()
    assert '"name": "Test User"' in mock_stdout.getvalue()

if __name__ == '__main__':
    pytest.main()