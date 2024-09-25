import pytest
from unittest.mock import Mock, patch
from peepdb.core import peep_db
from peepdb.config import save_connection, get_connection, list_connections, remove_connection, remove_all_connections
from peepdb.db import MySQLDatabase, PostgreSQLDatabase, MariaDBDatabase

@pytest.fixture
def mock_db():
    db = Mock()
    db.fetch_tables.return_value = ['table1', 'table2']
    db.fetch_data.return_value = {
        'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}],
        'page': 1,
        'total_pages': 1,
        'total_rows': 2
    }
    return db

@patch('peepdb.core.MySQLDatabase')
@patch('peepdb.core.PostgreSQLDatabase')
@patch('peepdb.core.MariaDBDatabase')
def test_peep_db(mock_mariadb, mock_postgresql, mock_mysql, mock_db):
    mock_mysql.return_value = mock_db
    mock_postgresql.return_value = mock_db
    mock_mariadb.return_value = mock_db

    # Test MySQL
    result = peep_db('mysql', 'host', 'user', 'password', 'database', format='json')
    assert result == {
        'table1': {'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}], 'page': 1, 'total_pages': 1, 'total_rows': 2},
        'table2': {'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}], 'page': 1, 'total_pages': 1, 'total_rows': 2}
    }

    # Test PostgreSQL
    result = peep_db('postgres', 'host', 'user', 'password', 'database', table='table1', format='json')
    assert result == {
        'table1': {'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}], 'page': 1, 'total_pages': 1, 'total_rows': 2}
    }

    # Test MariaDB
    result = peep_db('mariadb', 'host', 'user', 'password', 'database', format='json')
    assert result == {
        'table1': {'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}], 'page': 1, 'total_pages': 1, 'total_rows': 2},
        'table2': {'data': [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}], 'page': 1, 'total_pages': 1, 'total_rows': 2}
    }

    # Test unsupported database type
    with pytest.raises(ValueError):
        peep_db('unsupported', 'host', 'user', 'password', 'database')

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