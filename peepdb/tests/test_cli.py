import pytest
from click.testing import CliRunner
from peepdb.cli import cli
from unittest.mock import patch, MagicMock

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.fetch_tables.return_value = ['users', 'products']
    db.fetch_data.return_value = {
        'data': [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Smith'}
        ],
        'page': 1,
        'total_pages': 1,
        'total_rows': 2
    }
    return db

@patch('peepdb.cli.get_connection')
@patch('peepdb.core.MySQLDatabase')
def test_view_command_with_pagination(mock_mysql_db, mock_get_connection, runner, mock_db):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_mysql_db.return_value = mock_db
    mock_db.fetch_data.return_value = {
        'data': [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}],
        'page': 2,
        'total_pages': 3,
        'total_rows': 100
    }

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--page', '2', '--page-size', '50'])

    assert result.exit_code == 0
    assert "Table: users" in result.output
    assert "John Doe" in result.output
    assert "Jane Smith" in result.output
    assert "Page 2 of 3" in result.output
    assert "Total rows: 100" in result.output

    mock_get_connection.assert_called_once_with('testconn')
    mock_db.fetch_data.assert_called_once_with('users', 2, 50)

@patch('peepdb.cli.get_connection')
@patch('peepdb.core.MySQLDatabase')
def test_view_command_with_json_format(mock_mysql_db, mock_get_connection, runner, mock_db):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_mysql_db.return_value = mock_db

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--format', 'json'])

    assert result.exit_code == 0
    assert '"data": [' in result.output
    assert '"id": 1' in result.output
    assert '"name": "John Doe"' in result.output
    assert '"page": 1' in result.output
    assert '"total_rows": 2' in result.output

@patch('peepdb.cli.get_connection')
@patch('peepdb.core.MySQLDatabase')
def test_view_command_with_scientific(mock_mysql_db, mock_get_connection, runner, mock_db):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_mysql_db.return_value = mock_db

    # Modify the mock data to include a large number to test scientific notation
    mock_db.fetch_data.return_value = {
        'data': [{'id': 1, 'salary': 1234567890}, {'id': 2, 'salary': 9876543210}],
        'page': 1,
        'total_pages': 1,
        'total_rows': 2
    }

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--scientific'])

    assert result.exit_code == 0
    assert "Table: users" in result.output
    assert any(scientific in result.output for scientific in ["1.234568e+09", "1.23457e+09"])  # Ensure salary is displayed in scientific notation
    assert any(scientific in result.output for scientific in ["9.876543e+09", "9.87654e+09"])

    mock_get_connection.assert_called_once_with('testconn')

@patch('peepdb.cli.get_connection')
def test_view_command_invalid_connection(mock_get_connection, runner):
    mock_get_connection.return_value = None

    result = runner.invoke(cli, ['view', 'invalid_conn', '--table', 'users'])

    assert result.exit_code == 0
    assert "Error: No saved connection found with name 'invalid_conn'." in result.output

@patch('peepdb.cli.save_connection')
def test_save_command(mock_save_connection, runner):
    result = runner.invoke(cli, [
        'save', 
        'testconn', 
        '--db-type', 'mysql', 
        '--host', 'localhost', 
        '--user', 'testuser', 
        '--password', 'testpassword',  # Include the password as a command-line option
        '--database', 'testdb'
    ])
    
    if result.exit_code != 0:
        print(f"Command output: {result.output}")
        print(f"Exception: {result.exception}")

    assert result.exit_code == 0
    mock_save_connection.assert_called_once_with('testconn', 'mysql', 'localhost', 'testuser', 'testpassword', 'testdb')

@patch('peepdb.cli.list_connections')
def test_list_command(mock_list_connections, runner):
    mock_list_connections.return_value = None  # The function prints directly, so we return None

    result = runner.invoke(cli, ['list'])

    assert result.exit_code == 0
    mock_list_connections.assert_called_once()

@patch('peepdb.cli.remove_connection')
def test_remove_command(mock_remove_connection, runner):
    mock_remove_connection.return_value = True

    result = runner.invoke(cli, ['remove', 'testconn'], input='y\n')

    assert result.exit_code == 0
    assert "Connection 'testconn' has been removed." in result.output
    mock_remove_connection.assert_called_once_with('testconn')

@patch('peepdb.cli.remove_all_connections')
def test_remove_all_command(mock_remove_all_connections, runner):
    mock_remove_all_connections.return_value = 2

    result = runner.invoke(cli, ['remove-all'], input='y\n')

    assert result.exit_code == 0
    assert "2 connection(s) have been removed." in result.output
    mock_remove_all_connections.assert_called_once()

if __name__ == '__main__':
    pytest.main()