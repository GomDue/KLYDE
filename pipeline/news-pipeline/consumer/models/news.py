from pydantic import BaseModel
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    link: str
    description: Optional[str] = None
    published: str
    author: Optional[str] = None
    content: str
    source: Optional[str] = None
    