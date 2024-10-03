import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Any
from .base import BaseDatabase
import logging

logger = logging.getLogger(__name__)

class FirebaseDatabase(BaseDatabase):
    def __init__(self, service_account_path: str, **kwargs):
        self.service_account_path = service_account_path
        self.kwargs = kwargs
        self.db = None

    def connect(self):
        try:
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(self.service_account_path)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logger.debug("Connected to Firebase Firestore")
        except Exception as e:
            logger.error(f"Failed to connect to Firebase: {e}")
            raise ConnectionError(f"Failed to connect to Firebase: {e}")

    def disconnect(self):
        # Firebase Admin SDK does not provide a disconnect method
        pass

    def fetch_tables(self) -> List[str]:
        try:
            # In Firestore, collections are equivalent to tables
            collections = self.db.collections()
            return [collection.id for collection in collections]
        except Exception as e:
            logger.error(f"Failed to fetch collections: {e}")
            raise e

    def fetch_data(self, table_name: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        try:
            collection_ref = self.db.collection(table_name)
            documents = collection_ref.stream()
            data = [doc.to_dict() for doc in documents]

            # Implement pagination manually
            total_rows = len(data)
            total_pages = (total_rows + page_size - 1) // page_size  # Ceiling division
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            page_data = data[start_index:end_index]

            return {
                'data': page_data,
                'page': page,
                'total_pages': total_pages,
                'total_rows': total_rows
            }
        except Exception as e:
            logger.error(f"Failed to fetch data from '{table_name}': {e}")
            raise e