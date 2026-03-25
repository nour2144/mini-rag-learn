from ..helper.config import get_settings, Settings

class BaseDBModel:
    def __init__(self, db):
        self.db = db
        self.app_settings = get_settings()