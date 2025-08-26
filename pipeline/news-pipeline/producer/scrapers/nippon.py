from fetchers.common import get_soup

def extract_content(link: str) -> str:
    soup = get_soup(link)
    paras = soup.select("div.editArea > p")
    texts = [p.get_text(strip=True) for p in paras if not p.has_attr("class")]
    return " ".join(texts)
