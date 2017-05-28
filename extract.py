import requests
import lxml.html


class article:
    def __init__(self):
        self.article_text = []

    def get_article(self, target_url):
        target_html = requests.get(target_url).text
        root = lxml.html.fromstring(target_html)
        articles = [p.text_content() for p in root.cssselect('.article > p')]
        self.article_text = ''.join(articles)



