import pytest
from unittest.mock import Mock, patch
from peepdb.core import peep_db, connect_to_database, fetch_tables, view_table
from peepdb.config import save_connection, get_connection, list_connections, remove_connection, remove_all_connections

# Mock database connection
@pytest.fixture
def mock_db_connection():
    return Mock()

# Mock cursor
@pytest.fixture
def mock_cursor():
    cursor = Mock()
    cursor.fetchall.return_value = [('table1',), ('table2',)]
    cursor.description = [('column1',), ('column2',)]
    return cursor

@patch('peepdb.core.mysql.connector.connect')
@patch('peepdb.core.psycopg2.connect')
@patch('peepdb.core.pymysql.connect')
def test_connect_to_database(mock_pymysql, mock_psycopg2, mock_mysql):
    # Test MySQL connection
    connect_to_database('mysql', 'host', 'user', 'password', 'database')
    mock_mysql.assert_called_once_with(host='host', user='user', password='password', database='database', port=3306)

    # Reset the mock
    mock_mysql.reset_mock()

    # Test with custom port
    connect_to_database('mysql', 'host', 'user', 'password', 'database', port=3307)
    mock_mysql.assert_called_once_with(host='host', user='user', password='password', database='database', port=3307)

    # Test PostgreSQL connection
    connect_to_database('postgres', 'host', 'user', 'password', 'database')
    mock_psycopg2.assert_called_once_with(host='host', user='user', password='password', database='database', port=5432)

    # Test MariaDB connection
    connect_to_database('mariadb', 'host', 'user', 'password', 'database')
    mock_pymysql.assert_called_once_with(host='host', user='user', password='password', database='database', port=3306)

    # Test unsupported database type
    with pytest.raises(ValueError):
        connect_to_database('unsupported', 'host', 'user', 'password', 'database')

# Test fetch_tables function
def test_fetch_tables(mock_cursor):
    assert fetch_tables(mock_cursor, 'mysql') == ['table1', 'table2']
    mock_cursor.execute.assert_called_once_with("SHOW TABLES")

    mock_cursor.reset_mock()
    assert fetch_tables(mock_cursor, 'postgres') == ['table1', 'table2']
    mock_cursor.execute.assert_called_once_with("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

# Test view_table function
def test_view_table(mock_cursor):
    mock_cursor.fetchall.return_value = [(1, 'value1'), (2, 'value2')]
    result = view_table(mock_cursor, 'test_table')
    assert result == [{'column1': 1, 'column2': 'value1'}, {'column1': 2, 'column2': 'value2'}]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table")

# Updated test_peep_db function
@patch('peepdb.core.connect_to_database')
@patch('peepdb.core.fetch_tables')
@patch('peepdb.core.view_table')
def test_peep_db(mock_view_table, mock_fetch_tables, mock_connect):
    mock_connect.return_value.cursor.return_value = Mock()
    mock_fetch_tables.return_value = ['table1', 'table2']
    mock_view_table.return_value = ['row1']  # Changed this line

    # Test without specifying a table
    result = peep_db('mysql', 'host', 'user', 'password', 'database', format='json')
    assert result == {'table1': ['row1'], 'table2': ['row1']}

    # Test with a specific table
    result = peep_db('mysql', 'host', 'user', 'password', 'database', table='table1', format='json')
    assert result == {'table1': ['row1']}

    # Verify that view_table was called with the correct arguments
    mock_view_table.assert_called_with(mock_connect.return_value.cursor.return_value, 'table1')

# Test configuration functions
@patch('peepdb.config.os.path.exists')
@patch('peepdb.config.open')
@patch('peepdb.config.json.load')
@patch('peepdb.config.json.dump')
@patch('peepdb.config.encrypt')
@patch('peepdb.config.decrypt')
def test_config_functions(mock_decrypt, mock_encrypt, mock_json_dump, mock_json_load, mock_open, mock_exists):
    # Test save_connection
    mock_exists.return_value = True
    mock_json_load.return_value = {}
    mock_encrypt.side_effect = lambda x: f'encrypted_{x}'

    save_connection('test_conn', 'mysql', 'host', 'user', 'password', 'database')
    mock_json_dump.assert_called_once()

    # Test get_connection
    mock_json_load.return_value = {
        'test_conn': {
            'db_type': 'mysql',
            'host': 'encrypted_host',
            'user': 'encrypted_user',
            'password': 'encrypted_password',
            'database': 'encrypted_database'
        }
    }
    mock_decrypt.side_effect = lambda x: x.replace('encrypted_', '')

    result = get_connection('test_conn')
    assert result == ('mysql', 'host', 'user', 'password', 'database')

    # Test list_connections
    list_connections()
    # Assert that print was called with the correct arguments

    # Test remove_connection
    mock_json_load.return_value = {'test_conn': {}, 'other_conn': {}}
    assert remove_connection('test_conn') == True
    mock_json_dump.assert_called()

    # Test remove_all_connections
    mock_json_load.return_value = {'test_conn': {}, 'other_conn': {}}
    assert remove_all_connections() == 2
    # Assert that os.remove was called with the correct arguments

if __name__ == '__main__':
    pytest.main()