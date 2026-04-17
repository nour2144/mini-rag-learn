from .VectorDBFactory import VectorDBFactory
from .VectorDBEnums import VectorDBEnum
from .providers import QdrantProvider
from controllers.base_controller import BaseController
class VectorDBProvider():
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()
    def create_provider(self, provider_name: str):
        if provider_name == VectorDBEnum.MODE_ONLINE.value:
            return QdrantProvider(
                url=self.config.qdrant_url,
                api_key=self.config.qdrant_api_key,
                distance_method=self.config.vector_db_distance_method
            )
        if provider_name == VectorDBEnum.MODE_OFFLINE.value:
            return QdrantProvider(
                db_path=self.base_controller.get_db_default_path(self.config.qdrant_db_path),
                distance_method=self.config.vector_db_distance_method
            )
        else:
            raise ValueError(f"Unsupported VectorDB provider type: {provider_name}")
        
                