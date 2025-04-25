from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def preprocess_content(content):
    """
    데이터 전처리 - 텍스트 길이 제한  (5000 토큰)
    토큰 수를 제한하여 처리 효율성 확보
    """
    import tiktoken

    if not content:
        return ""
        
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    
    if len(tokens) > 5000:
        truncated_tokens = tokens[:5000]
        return encoding.decode(truncated_tokens)
    
    return encoding.decode(tokens)


def transform_extract_keywords(text):
    """
    텍스트 데이터 변환 - 키워드 5개 추출  
    입력 텍스트에서 핵심 키워드를 추출하는 변환 로직
    """
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
    """
    텍스트 데이터 변환 - 벡터 임베딩  
    텍스트를 수치형 벡터로 변환하는 변환 로직
    """
    client = OpenAI()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def transform_classify_category(content):
    """
    텍스트 데이터 변환 - 카테고리 분류  
    뉴스 내용을 기반으로 적절한 카테고리로 분류하는 변환 로직
    """
    categories = [
        "IT_과학", "건강", "경제", "교육", "국제", "라이프스타일", "문화", "사건사고",
        "사회일반", "산업", "스포츠", "여성복지", "여행레저", "연예", "정치", "지역", "취미"
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

    model_output = response.choices[0].message.content.strip()

    if model_output not in categories:
        model_output = "미분류"

    return model_output

