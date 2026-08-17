from pydantic import BaseModel
from typing import Any

class SettingsUpdate(BaseModel):
    settings: Any
