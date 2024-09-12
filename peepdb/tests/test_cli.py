import pytest
from click.testing import CliRunner
from peepdb.cli import cli, view, save, remove, remove_all
from unittest.mock import patch, MagicMock

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'peepDB: A quick database table viewer.' in result.output

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = "Mocked table data"

    result = runner.invoke(cli, ['view', 'testconn'])
    assert result.exit_code == 0
    assert "Mocked table data" in result.output

    mock_get_connection.assert_called_once_with('testconn')
    mock_peep_db.assert_called_once_with('mysql', 'localhost', 'user', 'password', 'testdb', None, format='table')

@patch('peepdb.cli.save_connection')
def test_save_command(mock_save_connection, runner):
    result = runner.invoke(cli, ['save', 'testconn', '--db-type', 'mysql', '--host', 'localhost', 
                                 '--user', 'testuser', '--password', 'testpass', '--database', 'testdb'])
    assert result.exit_code == 0
    assert "Connection 'testconn' saved successfully." in result.output
    mock_save_connection.assert_called_once_with('testconn', 'mysql', 'localhost', 'testuser', 'testpass', 'testdb')

@patch('peepdb.cli.list_connections')
def test_list_command(mock_list_connections, runner):
    mock_list_connections.return_value = None  # Assuming it prints directly
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

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_with_table_and_format(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = {"users": [{"id": 1, "name": "Test User"}]}

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--format', 'json'])
    assert result.exit_code == 0
    assert '"name": "Test User"' in result.output

    mock_get_connection.assert_called_once_with('testconn')
    mock_peep_db.assert_called_once_with('mysql', 'localhost', 'user', 'password', 'testdb', 'users', format='json')

def test_save_command_password_prompt(runner):
    result = runner.invoke(cli, ['save', 'testconn', '--db-type', 'mysql', '--host', 'localhost', 
                                 '--user', 'testuser', '--database', 'testdb'],
                           input='secretpassword\n')
    assert result.exit_code == 0
    assert "Connection 'testconn' saved successfully." in result.output

if __name__ == '__main__':
    pytest.main()