from scrapers import bbc, nippon, nyt, zdnet

NEWS_SOURCES = [
    {
        "name": "BBC",
        "rss_url": "http://feeds.bbci.co.uk/news/rss.xml",
        "scraper": bbc.extract_content
    },
    {
        "name": "Nippon", 
        "rss_url": "https://www.nippon.com/en/feed/",
        "scraper": nippon.extract_content
    },
    {
        "name": "NYT",  
        "rss_url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "scraper": nyt.extract_content
    },
    {
        "name": "ZDNet",
        "rss_url": "https://www.zdnet.com/news/rss.xml",
        "scraper": zdnet.extract_content
    },
]
