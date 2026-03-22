from .base_controller import BaseController
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..enums.ResponseEnum import ResponseEnum
import magic
class DataController(BaseController):
    def __init__(self):
        super().__init__()
    
    async def validate_file(self, file):
        # Implement file validation logic 
        file_bytes = await file.read(2048)
        self.file_type = magic.from_buffer(file_bytes, mime=True)
        if self.file_type not in self.app_settings.file_allowed_types:
            raise HTTPException(status_code=400, detail=ResponseEnum.FILE_TYPE_UNSUPPORTED.value)
        
        if file.size > self.app_settings.file_max_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=ResponseEnum.FILE_SIZE_EXCEEDED.value)
        return JSONResponse(content={"file_name": file.filename, "file_type": self.file_type, "signal": ResponseEnum.FILE_VALIDATION_SUCCESS.value}, status_code=200)