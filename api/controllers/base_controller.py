from ..helper.config import get_settings
import os
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.files_default_path = os.path.join(self.base_dir, f"assets/{self.app_settings.folder_default_name}")
        self.db_default_path = os.path.join(self.base_dir, f"assets/db")
        if not os.path.exists(self.files_default_path):
            os.makedirs(self.files_default_path, exist_ok=True)
    def get_db_default_path(self, db_path: str = None):
        db_path = os.path.join(self.db_default_path, db_path) if db_path else self.db_default_path
        if not os.path.exists(db_path):
            os.makedirs(db_path, exist_ok=True)
        return db_path
        



