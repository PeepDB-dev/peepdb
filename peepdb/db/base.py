from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

class BaseDatabase(ABC):
    def __init__(self, host: str, user: str, password: str, database: str, port: int = None, **kwargs):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.extra_params = kwargs
        self.connection = None
        self.cursor = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def fetch_tables(self) -> List[str]:
        pass

    @abstractmethod
    def fetch_data(self, table: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()