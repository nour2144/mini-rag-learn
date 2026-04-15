from .BaseDBModel import BaseDBModel
from ..enums import CollectionsEnum
from .db_schemes import AssetDB
from fastapi import HTTPException, Path
from bson import ObjectId
class AssetModel(BaseDBModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = self.db[CollectionsEnum.Collections_ASSETS.value]
    @classmethod
    async def create_instance(cls, db):
        """Factory method to create an instance of FolderModel and initialize the collection."""
        instance = cls(db)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        """Initializes the collection by creating necessary indexes."""
        all_collections = await self.db.list_collection_names()
        if CollectionsEnum.Collections_ASSETS.value not in all_collections:
            self.db[CollectionsEnum.Collections_ASSETS.value]
            indexes = AssetDB.get_indexes()
            for index in indexes:
                self.collection.create_index(index["key"], name=index["name"], unique=index.get("unique", True))
                
    async def create_asset(self, asset: AssetDB):
        """Creates a new asset document in the database."""
        result = await self.collection.insert_one(asset.dict())
        asset._id = result.inserted_id
        return asset, str(asset._id)
    async def get_all_assets(self, asset_folder_id: str, asset_type: str = None):
        """Retrieves all asset documents from the database."""
        query = {"asset_folder_id": ObjectId(asset_folder_id)}
        if asset_type is not None:
            query["asset_type"] = asset_type
        records = await self.collection.find(query).to_list(length=None)
        return [AssetDB(**record) for record in records]
    async def get_asset(self, asset_folder_id, asset_name: str):
        """Retrieves an asset document by its ID."""
        asset_data = await self.collection.find_one({
            "asset_folder_id": ObjectId(asset_folder_id),
            "asset_name": asset_name
        })
        if asset_data:
            return AssetDB(**asset_data)
        return None