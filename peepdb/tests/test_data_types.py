import pytest
from unittest.mock import Mock, patch
from datetime import date, time, datetime
from decimal import Decimal
from peepdb.core import view_table, peep_db

import pytest
from unittest.mock import Mock, patch
from datetime import date, time, datetime
from decimal import Decimal
from peepdb.core import view_table, peep_db
import json

@pytest.fixture
def mock_cursor():
    cursor = Mock()
    cursor.description = [
        ('id', 'INT'),
        ('name', 'VARCHAR'),
        ('birth_date', 'DATE'),
        ('wake_time', 'TIME'),
        ('last_login', 'DATETIME'),
        ('balance', 'DECIMAL'),
        ('is_active', 'BOOLEAN'),
        ('data', 'JSON')
    ]
    cursor.fetchone.return_value = (2,)  # Mock the total number of rows
    return cursor


def test_peep_db_with_data_types(mock_cursor):
    with patch('peepdb.core.connect_to_database') as mock_connect:
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'John Doe', date(1990, 1, 1), time(8, 0), datetime(2023, 5, 1, 12, 30), Decimal('1000.50'), True,
             '{"key": "value"}'),
            (2, 'Jane Smith', date(1985, 5, 15), time(7, 30), datetime(2023, 5, 2, 9, 45), Decimal('2500.75'), False,
             '["item1", "item2"]')
        ]

        result = peep_db('mysql', 'host', 'user', 'password', 'database', table='test_table', format='json')

        # Parse the JSON result
        result_dict = json.loads(result)

        assert 'test_table' in result_dict
        assert len(result_dict['test_table']['data']) == 2
        # Add more assertions as needed


def test_view_table_null_values(mock_cursor):
    mock_cursor.fetchall.return_value = [
        (1, None, None, None, None, None, None, None)
    ]

    result = view_table(mock_cursor, 'test_table')

    assert len(result['data']) == 1
    assert result['data'][0] == {
        'id': 1,
        'name': None,
        'birth_date': None,
        'wake_time': None,
        'last_login': None,
        'balance': None,
        'is_active': None,
        'data': None
    }
    assert result['page'] == 1
    assert result['total_pages'] == 1
    assert result['total_rows'] == 2


if __name__ == '__main__':
    pytest.main()
