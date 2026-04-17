from abc import ABC, abstractmethod

class VectorDBFactory(ABC):
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass
    @abstractmethod
    def list_collections(self) -> list:
        pass
    @abstractmethod
    def get_collection(self, collection_name: str) -> dict:
        pass
    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass
    @abstractmethod
    def create_collection(self, collection_name: str, embedding_dim: int, do_reset: bool = False):
        pass
    @abstractmethod
    def insert_one(self, text: str, embedding: list, metadata: dict, collection_name: str, vector_id: str = None):
        pass
    @abstractmethod
    def insert_many(self, texts: list, embeddings: list, metadatas: list, collection_name: str, vector_ids: list = None, batch_size: int = 50):
        pass
    @abstractmethod
    def search_vector(self, query_embedding: list, collection_name: str, limit: int) -> list:
        pass