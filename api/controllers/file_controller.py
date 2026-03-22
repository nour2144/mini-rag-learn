#libraries
from .base_controller import BaseController
import os
# code
class FileController(BaseController):
    def __init__(self):
        super().__init__()
        
    def get_folder_path(self, folder_id: str):
        folder_path = os.path.join(self.files_default_path, folder_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def get_file_path(self, folder_id: str, file_id: str):
        folder_path = self.get_folder_path(folder_id)
        file_path = os.path.join(folder_path, file_id)
        return file_path