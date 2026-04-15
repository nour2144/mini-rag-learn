from api.models.db_schemes.BaseDB import BaseDB
from pydantic import Field, field_validator

class FolderDB(BaseDB):
    folder_id: str = Field(..., description="Unique identifier for the folder")

    @field_validator('folder_id')
    def validate_folder_id(cls, value):
        if not value.isalnum():
            raise ValueError("folder_id must be alphanumeric")
        return value
    @classmethod
    def get_indexes(cls):
        return [
            {
                "key" : [("folder_id", 1)],
                "name" : "folder_id_index",
                "unique" : True
            }
        ]
        