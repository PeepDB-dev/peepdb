import pytest
from unittest.mock import Mock, patch
from datetime import date, time, datetime
from decimal import Decimal
from peepdb.core import view_table, peep_db


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
        ('data', 'JSON'),
        ('atomic_mass', 'DECIMAL'),
        ('other_number', 'DECIMAL')
    ]
    cursor.fetchone.return_value = (2,)  # Mock the total number of rows
    return cursor


def test_peep_db_with_data_types(mock_cursor):
    with patch('peepdb.core.connect_to_database') as mock_connect:
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (
                1,
                'John Doe',
                date(1990, 1, 1),
                time(8, 0),
                datetime(2023, 5, 1, 12, 30),
                Decimal('1000.50'),
                True,
                '{"key": "value"}',
                Decimal('1.008'),
                Decimal('2e+20')
            ),
            (
                2,
                'Jane Smith',
                date(1985, 5, 15),
                time(7, 30),
                datetime(2023, 5, 2, 9, 45),
                Decimal('2500.75'),
                False,
                '["item1", "item2"]',
                Decimal('4.0026'),
                Decimal('3e+22')
            )
        ]

        result = peep_db('mysql', 'host', 'user', 'password', 'database', table='test_table', format='json')

        assert 'test_table' in result
        assert len(result['test_table']['data']) == 2
        assert result['test_table']['data'][0] == {
            'id': 1,
            'name': 'John Doe',
            'birth_date': '1990-01-01',
            'wake_time': '08:00:00',
            'last_login': '2023-05-01T12:30:00',
            'balance': 1000.50,
            'is_active': True,
            'data': '{"key": "value"}',
            'atomic_mass': 1.008,
            'other_number': 2e+20
        }
        assert result['test_table']['page'] == 1
        assert result['test_table']['total_pages'] == 1
        assert result['test_table']['total_rows'] == 2


def test_view_table_scientific_enabled(mock_cursor):
    # Mocking data with numeric values for scientific notation test
    mock_cursor.fetchall.return_value = [
        (
            1,
            'Hydrogen',
            None,
            None,
            None,
            None,
            None,
            None,
            Decimal('1.008'),
            Decimal('2e+20')
        ),
        (
            2,
            'Helium',
            None,
            None,
            None,
            None,
            None,
            None,
            Decimal('4.0026'),
            Decimal('3e+22')
        )
    ]

    # Test with scientific notation enabled
    result = view_table(mock_cursor, 'test_table', scientific=True)

    assert len(result['data']) == 2
    assert result['data'][0] == {
        'id': 1.0,  # Expect float in scientific format
        'name': 'Hydrogen',
        'birth_date': None,
        'wake_time': None,
        'last_login': None,
        'balance': None,
        'is_active': None,
        'data': None,
        'atomic_mass': 1.008,
        'other_number': 2e+20
    }
    assert result['data'][1] == {
        'id': 2.0,
        'name': 'Helium',
        'birth_date': None,
        'wake_time': None,
        'last_login': None,
        'balance': None,
        'is_active': None,
        'data': None,
        'atomic_mass': 4.0026,
        'other_number': 3e+22
    }
    assert result['page'] == 1
    assert result['total_pages'] == 1
    assert result['total_rows'] == 2


def test_view_table_scientific_disabled(mock_cursor):
    # Mocking data with numeric values for scientific notation test
    mock_cursor.fetchall.return_value = [
        (
            1,
            'Hydrogen',
            None,
            None,
            None,
            None,
            None,
            None,
            Decimal('1.008'),
            Decimal('2e+20')
        ),
        (
            2,
            'Helium',
            None,
            None,
            None,
            None,
            None,
            None,
            Decimal('4.0026'),
            Decimal('3e+22')
        )
    ]

    # Test with scientific notation disabled
    result = view_table(mock_cursor, 'test_table', scientific=False)

    assert len(result['data']) == 2
    assert result['data'][0] == {
        'id': 1,
        'name': 'Hydrogen',
        'birth_date': None,
        'wake_time': None,
        'last_login': None,
        'balance': None,
        'is_active': None,
        'data': None,
        'atomic_mass': 1.008,
        'other_number': 2e+20
    }
    assert result['data'][1] == {
        'id': 2,
        'name': 'Helium',
        'birth_date': None,
        'wake_time': None,
        'last_login': None,
        'balance': None,
        'is_active': None,
        'data': None,
        'atomic_mass': 4.0026,
        'other_number': 3e+22
    }
    assert result['page'] == 1
    assert result['total_pages'] == 1
    assert result['total_rows'] == 2


def test_view_table_null_values(mock_cursor):
    mock_cursor.fetchall.return_value = [
        (1, None, None, None, None, None, None, None, None, None)
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
        'data': None,
        'atomic_mass': None,
        'other_number': None
    }
    assert result['page'] == 1
    assert result['total_pages'] == 1
    assert result['total_rows'] == 2

