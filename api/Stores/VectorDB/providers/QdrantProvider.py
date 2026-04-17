from ..VectorDBFactory import VectorDBFactory
from ..VectorDBEnums import DistanceMethodEnum, VectorDBEnum
from qdrant_client import QdrantClient, models
class QdrantProvider(VectorDBFactory):
    def __init__(self, db_path: str = None, url: str = None, api_key: str = None, distance_method: str = None):
        self.client = None
        self.db_path = db_path
        self.url = url
        self.api_key = api_key
        self.distance_method = None
        self.set_distance_method(distance_method)

    def set_distance_method(self, distance_method: str):
        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = DistanceMethodEnum.COSINE.value
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = DistanceMethodEnum.DOT.value
        else:
            raise ValueError(f"Unsupported distance method: {distance_method}")

    def connect(self):
        if self.db_path:
            self.client = QdrantClient(path=self.db_path)
        elif self.url:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
    def disconnect(self):
        self.client = None
    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)
    def list_collections(self) -> list:
        return self.client.get_collections()
    def get_collection(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name)
    def delete_collection(self, collection_name: str) -> bool:
        if self.is_collection_exists(collection_name):
            self.client.delete_collection(collection_name)
            return True
        return False
    def create_collection(self, collection_name: str, embedding_dim: int, do_reset: bool = False):
        if do_reset:
            _ =  self.delete_collection(collection_name)
        if not self.is_collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "size": embedding_dim,
                    "distance": self.distance_method
                }
            )
            return True
        return False
    def insert_one(self, text: str, embedding: list, metadata: dict, collection_name: str, vector_id: str = None):
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                        models.Record(
                            vector=embedding,
                            payload={
                                "text": text,
                                "metadata": metadata
                            }
                        )
                    ]
                 )
        except Exception as e:
            print(f"Error occurred while inserting record: {e}")
            return False
        return True
    def insert_many(self, texts: list, embeddings: list, metadatas: list, collection_name: str, vector_ids: list = None, batch_size: int = 50):
        if metadatas is None:
            metadatas = [{}] * len(texts)
        try:
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                batch_embeddings = embeddings[i:i+batch_size]
                batch_metadatas = metadatas[i:i+batch_size]

                records = [
                    models.Record(
                        vector=embedding,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                    for text, embedding, metadata in zip(batch_texts, batch_embeddings, batch_metadatas)
                ]
                self.client.upload_records(collection_name=collection_name, records=records)
            return True
        except Exception as e:
            print(f"Error occurred while inserting records: {e}")
            return False
    def search_vector(self, query_embedding: list, collection_name: str, limit: int) -> list:
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Error occurred while searching vectors: {e}")
            return []