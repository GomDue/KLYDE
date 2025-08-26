from fetchers.common import get_soup

def extract_content(link: str) -> str:
    soup = get_soup(link)
    paras = soup.select('section[name="articleBody"] p')
    texts = [p.get_text(strip=True) for p in paras]
    return " ".join(texts)
    