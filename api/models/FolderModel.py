from .BaseDBModel import BaseDBModel
from ..enums import CollectionsEnum
from .db_schemes import FolderDB
from fastapi import HTTPException, Path
import math
class FolderModel(BaseDBModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = self.db[CollectionsEnum.Collections_FOLDERS.value]

    async def create_folder(self, folder: FolderDB):
        """Creates a new folder document in the database."""
        result = await self.collection.insert_one(folder.dict())
        folder._id = result.inserted_id
        return folder
    
    async def get_folder_or_creare_one(self, folder_id: str):
        """Retrieves a folder document by its ID or creates a new one if it doesn't exist."""
        folder_data = await self.collection.find_one({"folder_id": folder_id})
        if folder_data:
            return FolderDB(**folder_data)
        else:
            new_folder = FolderDB(folder_id=folder_id)
            folder = await self.create_folder(new_folder)
            return folder
    async def get_all_folders(self, page: int = 1, page_size: int = Path(..., gt=10, lt=100, description="Number of items per page")):
        """Retrieves all folder documents from the database."""
        total_documents = await self.collection.count_documents({})
        total_pages = math.ceil(total_documents / page_size)
        if page > total_pages and total_pages != 0:
            raise HTTPException(status_code=400, detail=f"Page {page} exceeds total pages {total_pages}.")
        cursor = self.collection.find({}).skip((page - 1) * page_size).limit(page_size)
        folders = []
        async for folder_data in cursor:
            folders.append(FolderDB(**folder_data))
        return folders, total_documents, total_pages
