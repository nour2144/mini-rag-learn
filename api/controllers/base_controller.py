from ..helper.config import get_settings
import os
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.files_default_path = os.path.join(self.base_dir, self.app_settings.folder_default_name)
        if not os.path.exists(self.files_default_path):
            os.makedirs(self.files_default_path, exist_ok=True)
        


