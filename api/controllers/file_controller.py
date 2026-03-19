#libraries
from .base_controller import BaseController
import os
# code
class FileController(BaseController):
    def __init__(self):
        super().__init__()
        
    def get_file_path(self, file_id):
        
        file_dir = os.path.join(self.files_default_path, file_id)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
        return file_dir