from api.models.db_schemes.BaseDB import BaseDB
from pydantic import Field, field_validator
from typing import Optional
from bson import ObjectId
class ChunksDB(BaseDB):
    chunk_text: str = Field(..., description="The text content of the chunk")
    chunk_metadata: dict = Field(..., description="Metadata associated with the chunk")
    chunk_order: int = Field(..., description="The order of the chunk within the folder", gt=0)
    chunk_folder_id: Optional[ObjectId] = Field(..., description="Reference to the folder containing this chunk")

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key" : [("chunk_folder_id", 1)],
                "name" : "chunk_folder_id_index",
                "unique" : False
            }
        ]