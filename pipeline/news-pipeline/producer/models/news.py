from pydantic import BaseModel

class NewsMessage(BaseModel):
    title: str | None = None
    link: str
    description: str | None = None
    published: str | None = None
    author: str | None = None
    content: str | None = None
    source: str | None = None
