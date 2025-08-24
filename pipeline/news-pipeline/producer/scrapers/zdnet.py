from fetchers.common import get_soup

def extract_content(link: str) -> str:
    soup = get_soup(link)
    paras = soup.select("div.c-articleContent p")
    texts = [p.get_text(strip=True) for p in paras if "zdnet" not in p.get_text(strip=True).lower()]
    return " ".join(texts)
