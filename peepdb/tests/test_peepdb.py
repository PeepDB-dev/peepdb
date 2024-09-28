import pytest
from unittest.mock import Mock, patch
from decimal import Decimal
from peepdb.core import peep_db
from peepdb.config import save_connection, get_connection, list_connections, remove_connection, remove_all_connections
from peepdb.db import MySQLDatabase, PostgreSQLDatabase, MariaDBDatabase, MongoDBDatabase

@patch('peepdb.core.MongoDBDatabase')
@patch('peepdb.core.MySQLDatabase')
@patch('peepdb.core.PostgreSQLDatabase')
@patch('peepdb.core.MariaDBDatabase')
def test_peep_db(mock_mariadb, mock_postgresql, mock_mysql, mock_mongodb):
    # Create a mock database object
    mock_db = Mock()
    mock_db.fetch_tables.return_value = ['table1', 'table2']
    mock_db.fetch_data.return_value = {
        'data': [
            {'id': 1, 'name': 'John', 'big_integer': 9223372036854775807, 'big_decimal': Decimal('9999999999999999.99')},
            {'id': 2, 'name': 'Jane', 'big_integer': 123456789, 'big_decimal': Decimal('1234.56789')}
        ],
        'page': 1,
        'total_pages': 1,
        'total_rows': 2
    }

    # Assign the mock database object to each database type
    mock_mysql.return_value = mock_db
    mock_postgresql.return_value = mock_db
    mock_mariadb.return_value = mock_db
    mock_mongodb.return_value = mock_db

    # Test MySQL without scientific notation
    result = peep_db('mysql', 'host', 'user', 'password', 'database', format='json', scientific=False)
    expected_result = {
        'table1': {
            'data': [
                {'id': 1, 'name': 'John', 'big_integer': 9223372036854775807, 'big_decimal': 1e+16},
                {'id': 2, 'name': 'Jane', 'big_integer': 123456789, 'big_decimal': 1234.56789}
            ],
            'page': 1,
            'total_pages': 1,
            'total_rows': 2
        },
        'table2': {
            'data': [
                {'id': 1, 'name': 'John', 'big_integer': 9223372036854775807, 'big_decimal': 1e+16},
                {'id': 2, 'name': 'Jane', 'big_integer': 123456789, 'big_decimal': 1234.56789}
            ],
            'page': 1,
            'total_pages': 1,
            'total_rows': 2
        }
    }
    assert result == expected_result

    # Test PostgreSQL without scientific notation
    result = peep_db('postgres', 'host', 'user', 'password', 'database', table='table1', format='json', scientific=False)
    expected_result_postgres = {
        'table1': {
            'data': [
                {'id': 1, 'name': 'John', 'big_integer': 9223372036854775807, 'big_decimal': 1e+16},
                {'id': 2, 'name': 'Jane', 'big_integer': 123456789, 'big_decimal': 1234.56789}
            ],
            'page': 1,
            'total_pages': 1,
            'total_rows': 2
        }
    }
    assert result == expected_result_postgres

    # Test MariaDB without scientific notation
    result = peep_db('mariadb', 'host', 'user', 'password', 'database', format='json', scientific=False)
    assert result == expected_result

    # Test MongoDB without scientific notation
    result = peep_db('mongodb', 'host', 'user', 'password', 'database', format='json', scientific=False)
    assert result == expected_result

    # Test MySQL with scientific notation
    result = peep_db('mysql', 'host', 'user', 'password', 'database', format='json', scientific=True)
    # Since scientific notation does not affect JSON output, the result should be the same
    assert result == expected_result

    # Test PostgreSQL with scientific notation
    result = peep_db('postgres', 'host', 'user', 'password', 'database', table='table1', format='json', scientific=True)
    assert result == expected_result_postgres

    # Test MariaDB with scientific notation
    result = peep_db('mariadb', 'host', 'user', 'password', 'database', format='json', scientific=True)
    assert result == expected_result

    # Test MongoDB with scientific notation
    result = peep_db('mongodb', 'host', 'user', 'password', 'database', format='json', scientific=True)
    assert result == expected_result

    # Test MySQL with scientific notation and table format
    result = peep_db('mysql', 'host', 'user', 'password', 'database', format='table', scientific=True)
    assert 'Table: table1' in result
    assert '9.223372e+18' in result or '9.22337e+18' in result
    assert '1.000000e+16' in result or '1e+16' in result

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
