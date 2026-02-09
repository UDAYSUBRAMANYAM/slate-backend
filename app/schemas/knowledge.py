from pydantic import BaseModel
from typing import Optional, List

class KnowledgeCreate(BaseModel):
    title: str
    content: str
    type: str
    tags: Optional[List[str]] = []
    source_url: Optional[str] = None

class KnowledgeResponse(KnowledgeCreate):
    id: int

    class Config:
        orm_mode = True
