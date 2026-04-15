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

    @classmethod
    async def create_instance(cls, db):
        """Factory method to create an instance of FolderModel and initialize the collection."""
        instance = cls(db)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        """Initializes the collection by creating necessary indexes."""
        all_collections = await self.db.list_collection_names()
        if CollectionsEnum.Collections_CHUNKS.value not in all_collections:
            self.db[CollectionsEnum.Collections_CHUNKS.value]
            indexes = ChunksDB.get_indexes()
            for index in indexes:
                self.collection.create_index(index["key"], name=index["name"], unique=index.get("unique", False))
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
        return len(chunks)