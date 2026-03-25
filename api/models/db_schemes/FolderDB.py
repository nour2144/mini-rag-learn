from api.models.db_schemes.BaseDB import BaseDB
from pydantic import Field, field_validator

class FolderDB(BaseDB):
    folder_id: str = Field(..., description="Unique identifier for the folder")

    @field_validator('folder_id')
    def validate_folder_id(cls, value):
        if not value.isalnum():
            raise ValueError("folder_id must be alphanumeric")
        return value