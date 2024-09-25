import pytest
from click.testing import CliRunner
from peepdb.cli import cli, view
from unittest.mock import patch, MagicMock
import json

@pytest.fixture
def runner():
    return CliRunner()


@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_with_pagination(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = "Mocked paginated data"

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--page', '2', '--page-size', '50'])

    assert result.exit_code == 0
    assert "Mocked paginated data" in result.output
    assert "Current Page: 2" in result.output
    assert "Next Page: peepdb view testconn --table users --page 3 --page-size 50" in result.output
    assert "Previous Page: peepdb view testconn --table users --page 1 --page-size 50" in result.output

    mock_get_connection.assert_called_once_with('testconn')
    mock_peep_db.assert_called_once_with(
        db_type='mysql',
        host='localhost',
        user='user',
        password='password',
        database='testdb',
        table='users',
        format='table',
        page=2,
        page_size=50
    )


@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_first_page(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = "Mocked first page data"

    result = runner.invoke(cli, ['view', 'testconn', '--table', 'users', '--page', '1', '--page-size', '10'])

    assert result.exit_code == 0
    assert "Mocked first page data" in result.output
    assert "Current Page: 1" in result.output
    assert "Next Page: peepdb view testconn --table users --page 2 --page-size 10" in result.output
    assert "Previous Page: peepdb view testconn --table users --page 0 --page-size 10" not in result.output  # Page 1 is the minimum

    # Adjust expected call
    mock_peep_db.assert_called_once_with(
        db_type='mysql',
        host='localhost',
        user='user',
        password='password',
        database='testdb',
        table='users',
        format='table',
        page=1,
        page_size=10
    )


@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_with_json_format(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = json.dumps({
        "data": [{"id": 1, "name": "Test"}],
        "page": 1,
        "total_pages": 1
    })

    result = runner.invoke(cli,
                           ['view', 'testconn', '--table', 'users', '--format', 'json', '--page', '1', '--page-size',
                            '10'])

    assert result.exit_code == 0
    assert '"data": [' in result.output
    assert '"page": 1' in result.output
    assert "Current Page:" not in result.output  # Navigation hints should not be present in JSON output

    # Optionally, assert that peep_db is called with correct parameters
    mock_peep_db.assert_called_once_with(
        db_type='mysql',
        host='localhost',
        user='user',
        password='password',
        database='testdb',
        table='users',
        format='json',
        page=1,
        page_size=10
    )


@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_invalid_connection(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = None

    result = runner.invoke(cli, ['view', 'invalid_conn', '--table', 'users', '--page', '1', '--page-size', '10'])

    assert result.exit_code == 0
    assert "Error: No saved connection found with name 'invalid_conn'." in result.output
    mock_peep_db.assert_not_called()

@patch('peepdb.cli.peep_db')
@patch('peepdb.cli.get_connection')
def test_view_command_default_values(mock_get_connection, mock_peep_db, runner):
    mock_get_connection.return_value = ('mysql', 'localhost', 'user', 'password', 'testdb')
    mock_peep_db.return_value = "Mocked default data"

    result = runner.invoke(cli, ['view', 'testconn'])

    assert result.exit_code == 0
    assert "Mocked default data" in result.output
    mock_peep_db.assert_called_once_with(
        db_type='mysql',
        host='localhost',
        user='user',
        password='password',
        database='testdb',
        table=None,
        format='table',
        page=1,
        page_size=100
    )


if __name__ == '__main__':
    pytest.main()
