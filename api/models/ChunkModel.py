from .BaseDBModel import BaseDBModel
from ..enums import CollectionsEnum
from .db_schemes import ChunksDB
from pymongo import InsertOne
from fastapi import HTTPException, Path
from bson import ObjectId
import math
class ChunkModel(BaseDBModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = self.db[CollectionsEnum.Collections_CHUNKS.value]
    async def create_chunk(self, chunks: ChunksDB):
        """Creates a new chunk document in the database."""
        result = await self.collection.insert_one(chunks.dict())
        chunks._id = result.inserted_id
        return chunks
    async def get_chunk(self, chunk_id: str):
        """Retrieves a chunk document by its ID."""
        chunk_data = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if chunk_data:
            return ChunksDB(**chunk_data)
        else:
            raise HTTPException(status_code=404, detail="Chunk not found.")
    async def insert_many_chunks(self, chunks: list[ChunksDB], batch_size: int = 30):
        """Inserts multiple chunk documents into the database."""
        [await self.collection.bulk_write([InsertOne(chunk.dict()) for chunk in batch]) for batch in [chunks[i:i + batch_size] for i in range(0, len(chunks), batch_size)]]
        return {"message": f"Inserted {len(chunks)} chunks successfully."}