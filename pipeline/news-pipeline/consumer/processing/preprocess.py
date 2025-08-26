import tiktoken
from openai import OpenAI


def preprocess_content(content):
    if not content:
        return ""
        
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    
    if len(tokens) > 5000:
        return encoding.decode(tokens[:5000])
    return encoding.decode(tokens)


def transform_extract_keywords(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "Read the following article and extract 5 key keywords that best represent the main topic of the news. Output only the keywords as a single comma-separated string. If the content is empty or missing, return an empty string."},
            {"role": "user", "content": text}
        ],
        max_tokens=100
    )
    keywords = response.choices[0].message.content.strip()
    return keywords.split(',')


def transform_to_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def transform_classify_category(content):
    categories = [
        "SciTech", "Health", "Economy", "Education", "International", "Lifestyle", "Culture", "Accidents",
        "Society", "Industry", "Sports", "Femcare", "TripLeisure", "Entertainment", "Politics", "Local", "Hobbies"
    ]

    prompt = f"""다음 뉴스 내용을 가장 적절한 카테고리로 분류해 주세요.
                가능한 카테고리 목록은 다음과 같습니다:
                {', '.join(categories)}

                뉴스 내용:
                {content}

                반드시 위 목록에서 하나만 선택해서 출력해주세요. 다른 설명 없이 카테고리 이름만 출력해주세요."""

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 텍스트를 분류하는 AI입니다. 주어진 뉴스 내용에 가장 적절한 카테고리를 정확히 하나 선택하세요."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20
    )

    return response.choices[0].message.content.strip()

