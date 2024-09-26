import pymongo
import pymongo.errors
from .base import BaseDatabase
import typing as t
from urllib.parse import quote_plus


class MongoDBDatabase(BaseDatabase):
    def connect(self) -> None:
        try:
            user = quote_plus(self.user)
            pwd = quote_plus(self.password)
            port = self.port or 27017
            mongo_uri = "mongodb://{}:{}@{}:{}/{}".format(
                user, pwd, self.host, port, self.database
            )

            if self.extra_params:
                params = '&'.join(
                    [f"{k}={v}" for k, v in self.extra_params.items]
                )

                mongo_uri = f"{mongo_uri}?{params}"

            self.conection = pymongo.MongoClient(mongo_uri)
            self.db = self.conection[self.database]
            self.logger.info(f"Connected to MongoDB database: {self.database}")
        except pymongo.errors.PyMongoError as e:
            self.logger.error(f"Error connecting to MongoDB database: {e}")
            raise

    def disconnect(self) -> None:
        if self.conection:
            self.conection.close()
            self.logger.info(
                f"Disconnected from MongoDB database: {self.database}"
            )

    def fetch_tables(self) -> t.List[str]:
        return self.db.list_collection_names()

    def fetch_data(
        self,
        table: str,
        page: int = 1,
        page_size: int = 100
    ) -> t.Dict[str, t.Any]:
        """
        Fetches data from the MongoDB database.
        """
        offset = (page -1) * page_size
        collection = self.db[table]
        data = list(collection.find({}).skip(offset).limit(page_size))
        total_rows = collection.count_documents({})

        rem = 1 if total_rows % page_size else 0
        total_pages = (total_rows // page_size) + rem

        return {
            'data': data,
            'page': page,
            'total_pages': total_pages,
            'total_rows': total_rows
        }
