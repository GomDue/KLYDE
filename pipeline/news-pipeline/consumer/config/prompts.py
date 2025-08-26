EXTRACT_KEYWORDS_SYSTEM = (
    "Read the following article and extract 5 key keywords that best represent "
    "the main topic of the news. Output only the keywords as a single comma-separated string. "
    "If the content is empty or missing, return an empty string."
)

CLASSIFY_CATEGORY_SYSTEM = (
    "당신은 텍스트를 분류하는 AI입니다. 주어진 뉴스 내용에 가장 적절한 카테고리를 정확히 하나 선택하세요."
)

CLASSIFY_CATEGORY_USER = (
    "다음 뉴스 내용을 가장 적절한 카테고리로 분류해 주세요.\n"
    "가능한 카테고리 목록은 다음과 같습니다:\n{categories}\n\n"
    "뉴스 내용:\n{text}\n\n"
    "반드시 위 목록에서 하나만 선택해서 출력해주세요. 다른 설명 없이 카테고리 이름만 출력해주세요."
)
