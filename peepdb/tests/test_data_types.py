import pytest
from unittest.mock import Mock, patch
from datetime import date, time, datetime
from decimal import Decimal
from peepdb.db import MySQLDatabase
from peepdb.core import peep_db

@pytest.fixture
def mock_db():
    db = Mock(spec=MySQLDatabase)
    db.fetch_data.return_value = {
        'data': [
            {
                'id': 1,
                'name': 'John Doe',
                'birth_date': date(1990, 1, 1),
                'wake_time': time(8, 0),
                'last_login': datetime(2023, 5, 1, 12, 30),
                'balance': Decimal('1000.50'),
                'is_active': True,
                'data': '{"key": "value"}'
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'birth_date': date(1985, 5, 15),
                'wake_time': time(7, 30),
                'last_login': datetime(2023, 5, 2, 9, 45),
                'balance': Decimal('2500.75'),
                'is_active': False,
                'data': '["item1", "item2"]'
            }
        ],
        'page': 1,
        'total_pages': 1,
        'total_rows': 2
    }
    return db

@patch('peepdb.core.MySQLDatabase')
def test_peep_db_with_data_types(mock_mysql_db):
    mock_db = Mock(spec=MySQLDatabase)
    mock_mysql_db.return_value = mock_db
    mock_db.fetch_data.return_value = {
        'data': [{
            'id': 1,
            'name': 'John Doe',
            'birth_date': date(1990, 1, 1),
            'wake_time': time(8, 0),
            'last_login': datetime(2023, 5, 1, 12, 30),
            'balance': 1000.50,
            'is_active': True,
            'data': '{"key": "value"}'
        }],
        'page': 1,
        'total_pages': 1,
        'total_rows': 1
    }

    result = peep_db('mysql', 'host', 'user', 'password', 'database', table='test_table', format='json')

    assert 'test_table' in result
    assert len(result['test_table']['data']) == 1
    
    expected_data = {
        'id': 1,
        'name': 'John Doe',
        'birth_date': '1990-01-01',
        'wake_time': '08:00:00',
        'last_login': '2023-05-01T12:30:00',
        'balance': 1000.50,
        'is_active': True,
        'data': '{"key": "value"}'
    }
    
    actual_data = result['test_table']['data'][0]
    
    # Compare each field individually
    for key, expected_value in expected_data.items():
        assert key in actual_data, f"Key '{key}' not found in actual data"
        actual_value = actual_data[key]
        
        if isinstance(expected_value, str) and isinstance(actual_value, (date, time, datetime)):
            assert expected_value == actual_value.isoformat(), f"Mismatch for key '{key}': expected {expected_value}, got {actual_value.isoformat()}"
        else:
            assert expected_value == actual_value, f"Mismatch for key '{key}': expected {expected_value}, got {actual_value}"
            
@patch('peepdb.core.MySQLDatabase')
def test_peep_db_with_large_numbers(mock_mysql_db):
    mock_db = Mock(spec=MySQLDatabase)
    mock_db.fetch_data.return_value = {
        'data': [
            {
                'id': 1,
                'big_integer': 9223372036854775807,
                'big_decimal': Decimal('9999999999999999.99')
            }
        ],
        'page': 1,
        'total_pages': 1,
        'total_rows': 1
    }
    mock_mysql_db.return_value = mock_db

    result = peep_db('mysql', 'host', 'user', 'password', 'database', table='test_table', format='json')

    assert 'test_table' in result
    assert len(result['test_table']['data']) == 1
    assert result['test_table']['data'][0] == {
        'id': 1,
        'big_integer': 9223372036854775807,
        'big_decimal': Decimal('9999999999999999.99')
    }

if __name__ == '__main__':
    pytest.main()