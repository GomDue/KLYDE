from pydantic import BaseModel
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    link: str
    published: str
    content: str
    description: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    