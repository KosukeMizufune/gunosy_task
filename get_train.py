import re
import time
import traceback

import lxml.html
import requests
from lxml.etree import XMLSyntaxError

from articleclass.models import Article


# 訓練データを取得しデータベースに保存する

def get_data(page_count):
    """
    トップページからそれぞれのカテゴリーの記事をクロールし、そのカテゴリーと記事をスクレイプしMongoDBに保存する関数

    :param page_count: int, スクレイプする予定の、各タグの記事一覧ページの数
    """
    session = requests.Session()
    response = session.get('https://gunosy.com/')
    urls = get_article_page(response, page_count)
    for url in urls:
        try:
            key = extract_key(url)
            key_match = Article.objects.filter(key=key)
            if not key_match:
                time.sleep(1)
                response = session.get(url)
                article = scrape_text(response)
                Article(tag=article['tag'], doc=article['doc'], key=article['key']).save()
                print(url)
        except KeyboardInterrupt:
            print('強制停止')
            break
        except IndexError:
            print(url)
            traceback.print_exc()
        except XMLSyntaxError:
            traceback.print_exc()


def extract_key(url):
    """
    同一の記事を取らないようにURLキーを識別するための関数

    :param url: str, スクレイプする記事のURL
    :return: str, URLの末尾のISBN
    """
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)


def scrape_tag_page(response):
    """
    トップページからそれぞれのカテゴリーのトップページのURLを取ってくる関数

    :param response: requests.models.Response, URLから読み込まれたwebページ
    :return: list, それぞれのカテゴリーのトップページのURL
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    url_tag = [a.get('href') for a in root.cssselect('.nav_list > * > a')[1:9]]
    return url_tag


def get_article_page(response, page_count):
    """
    それぞれのカテゴリーのトップページから100ページ目までの記事のURLを入手する関数

    :param response: requests.models.Response, URLから読み込まれたwebページ
    :param page_count: int, スクレイプする予定の、各タグの記事一覧ページの数
    """
    url_tag = scrape_tag_page(response)
    session = requests.Session()
    for url in url_tag:
        count = 1
        while count <= page_count[0]:
            response2 = session.get(url)
            root2 = lxml.html.fromstring(response2.content)
            root2.make_links_absolute(response2.url)
            for a in root2.cssselect('.list_title a'):
                url_article = a.get('href')
                yield url_article
            try:
                url = root2.cssselect('.btn')[0].get('href')
                count += 1
            except IndexError:
                traceback.print_exc()
                break
            time.sleep(1)
        time.sleep(1)


def scrape_text(response):
    """
    記事URLからタグと記事、識別キーをスクレイプする関数

    :param response: requests.models.Response, URLから読み込まれたwebページ
    :return: dict, 記事のタグとテキストデータ、識別キー
    """
    root3 = lxml.html.fromstring(response.text)
    text = [p.text_content() for p in root3.cssselect('.article > p')]
    doc = ''.join(text)
    article = {
        'tag': root3.cssselect('.breadcrumb_category'
                               ' span:nth-child(1)')[1].text_content(),
        'doc': doc,
        'key': extract_key(response.url)
    }
    return article
