from .base_controller import BaseController
from fastapi import HTTPException

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        # Initialize any additional attributes or services specific to DataController here
    
    def validate_file(self, file):
        # Implement file validation logic 
        if file.content_type not in self.app_settings.file_allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        
        if file.size > self.app_settings.max_file_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed size.")
        return True
