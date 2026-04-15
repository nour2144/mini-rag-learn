from api.models.db_schemes.BaseDB import BaseDB
from pydantic import Field, field_validator
from datetime import datetime
from bson import ObjectId

class AssetDB(BaseDB):
    asset_folder_id: ObjectId = Field(..., description="Unique identifier for the asset folder")
    asset_name: str = Field(..., description="Name of the asset")
    asset_type: str = Field(..., description="Type of the asset")
    asset_push_time: datetime = Field(datetime.now(), description="Time when the asset was pushed")

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key" : [("asset_folder_id", 1)],
                "name" : "asset_folder_id_index",
                "unique" : False
            }
            ,
            {
                "key" : [
                    ("asset_name", 1),
                    ("asset_folder_id", 1)
                    ],
                "name" : "asset_name_folder_id_index",
                "unique" : True
            }
        ]
        