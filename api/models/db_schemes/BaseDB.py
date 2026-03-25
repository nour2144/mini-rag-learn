from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class BaseDB(BaseModel):
    _id: Optional[ObjectId]
    
    class Config:
        arbitrary_types_allowed = True