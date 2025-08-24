from fetchers.common import get_soup

def extract_content(link: str) -> str:
    soup = get_soup(link)
    paras = soup.select('article div[data-component="text-block"] p')
    texts = [p.get_text(strip=True) for p in paras]
    return " ".join(texts)
