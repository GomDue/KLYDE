import requests
from bs4 import BeautifulSoup

_session: requests.Session | None = None

def session() -> requests.Session:
    global _session

    if _session is None:
        _session = requests.Session()

    return _session

def get_soup(url: str) -> BeautifulSoup:
    html = session().get(url).text
    return BeautifulSoup(html, "html.parser")
