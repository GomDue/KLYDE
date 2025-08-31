import tiktoken
from openai import OpenAI
from config.prompts import *
from config.settings import settings

# openai_client = OpenAI()


def preprocess_content(content: str) -> str:
    if not content:
        return ""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    return encoding.decode(tokens[:5000]) if len(tokens) > 5000 else encoding.decode(tokens)


def transform_extract_keywords(text) -> str:
    response = openai_client.chat.completions.create(
        model=settings.GPT_MODEL,
        messages=[
            {"role": "system",  "content": EXTRACT_KEYWORDS_SYSTEM},
            {"role": "user",    "content": text}
        ],
        max_tokens=100
    )
    keywords = response.choices[0].message.content.strip()
    return keywords.split(',')


def transform_to_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(input=text, model=settings.EMBEDDING_MODEL)
    return response.data[0].embedding


def transform_classify_category(content) -> str:
    response = openai_client.chat.completions.create(
        model=settings.GPT_MODEL,
        messages=[
            {"role": "system",  "content": CLASSIFY_CATEGORY_SYSTEM},
            {"role": "user",    "content": CLASSIFY_CATEGORY_USER.format(categories=settings.NEWS_CATEGORIES_STR, text=content)}
        ],
        max_tokens=20
    )

    return response.choices[0].message.content.strip()

