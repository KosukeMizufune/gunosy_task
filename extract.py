import requests
import lxml.html
from urllib.error import HTTPError, URLError


# 入力されたURLから記事を入手する関数
def get_article(target_url):
    if target_url is '' or target_url is None:
        return None
    try:
        target_html = requests.get(target_url).text
        root = lxml.html.fromstring(target_html)
        articles = \
            [p.text_content() for p in root.cssselect('.article > p')]
        article_text = ''.join(articles)
        return article_text
    except HTTPError:
        return None
    except URLError:
        return None
