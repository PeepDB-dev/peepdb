import pytest
from unittest.mock import patch, MagicMock
from peepdb.db.mongodb import MongoDBDatabase


def test_mongodb_connection_uri_generation():
    db = MongoDBDatabase(
        host='localhost',
        user='user name',
        password='p@ssword',
        database='mydb',
        port=1234,
        replicaSet='rs0'
    )
    mock_client = MagicMock()
    with patch('pymongo.MongoClient', return_value=mock_client) as mock_mc:
        db.connect()
        mock_mc.assert_called_once()
        uri = mock_mc.call_args.args[0]

    assert uri == 'mongodb://user+name:p%40ssword@localhost:1234/mydb?replicaSet=rs0'
    assert db.connection is mock_client
    assert db.db == mock_client.__getitem__.return_value
