from pydantic import BaseModel
from typing import Optional, List

class FactInput(BaseModel):
    user_id: str
    content: str
    tags: Optional[List[str]] = []

class DreamInput(BaseModel):
    user_id: str
    facts: Optional[List[str]] = None
