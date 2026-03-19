from .base_controller import BaseController
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..enums.ResponseEnum import ResponseEnum
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        # Initialize any additional attributes or services specific to DataController here
    
    def validate_file(self, file):
        # Implement file validation logic 
        if file.content_type not in self.app_settings.file_allowed_types:
            raise HTTPException(status_code=400, detail=ResponseEnum.FILE_TYPE_UNSUPPORTED.value)
        
        if file.size > self.app_settings.file_max_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=ResponseEnum.FILE_SIZE_EXCEEDED.value)
        return JSONResponse(content={"filename": file.filename, "content_type": file.content_type, "signal": ResponseEnum.FILE_VALIDATION_SUCCESS.value}, status_code=200)
