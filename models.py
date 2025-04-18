from pydantic import BaseModel

class NewsArticle(BaseModel):
    title: str
    link: str
    published: str
    content: str
