import mysql.connector
import psycopg2
import pymysql
from decimal import Decimal
from datetime import date, time, datetime
from tabulate import tabulate
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def connect_to_database(db_type, host, user, password, database, port=None, **kwargs):
    logger.debug(f"Attempting to connect to {db_type} database '{database}' on host '{host}' with user '{user}'")
    try:
        if db_type == 'mysql':
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database,
                                           port=port or 3306, **kwargs)
        elif db_type == 'postgres':
            conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=port or 5432,
                                    **kwargs)
        elif db_type == 'mariadb':
            conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port or 3306,
                                   **kwargs)
        else:
            raise ValueError("Unsupported database type")
        logger.debug("Connection successful")
        return conn
    except (mysql.connector.Error, psycopg2.Error, pymysql.Error) as e:
        logger.error(f"Failed to connect to {db_type} database: {str(e)}")
        raise ConnectionError(f"Failed to connect to {db_type} database: {str(e)}")
