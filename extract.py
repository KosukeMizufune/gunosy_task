import requests
import lxml.html
from urllib.error import HTTPError, URLError

# 入力されたURLから記事データを取ってくる関数 

class article:
    def __init__(self):
        self.article_text = []
    
    def get_article(self, target_url):
        if target_url is '' or target_url is None:
            return None
        try:
            target_html = requests.get(target_url).text
            root = lxml.html.fromstring(target_html)
            articles = [p.text_content() for p in root.cssselect('.article > p')]
            self.article_text = ''.join(articles)
        except HTTPError:
            return None
        except URLError:
            return None
            



