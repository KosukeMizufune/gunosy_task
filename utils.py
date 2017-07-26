from urllib.error import HTTPError, URLError
import lxml.html
import requests
from random import shuffle

import MeCab
from pymongo import MongoClient


def doctoword(doc):
    """
    URLから入手した記事を形態素解析する関数

    :param doc: str, URLから入手した記事のテキストデータ
    :return: list, 形態素解析された単語のベクトル
    """
    tagger = MeCab.Tagger("-Ochasen -d "
                          "/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    tagger.parse('')
    node = tagger.parseToNode(doc)
    words = []
    while node:
        split = node.feature.split(',')
        word_class, sub_word_class = split[:2]  # 品詞情報
        if word_class == '名詞' or word_class == '形容詞' \
                and sub_word_class in ('固有名詞', '一般'):
            if split[6] == '*':  # 一部の名詞（英語など）で要素[6]（原型）が"*"になるので
                words.append(node.surface)
            else:
                words.append(split[6])
        node = node.next
    return words


def get_article(target_url):
    """
    入力されたURLから記事を入手する関数

    :param target_url: str, フォームに入力されるURL
    :return: str, URL先のテキスト
    """
    if not target_url:
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


def get_train_data():
    """
    訓練データをカテゴリーと形態素解析された記事データに分ける関数

    :return tags: list, 記事のタグ
    :return: (list,list), 記事のテキストデータ
    """
    client = MongoClient('localhost')
    collection = client.scraping.article
    infos = [x for x in collection.find()]
    shuffle(infos)
    tags = []
    data = []
    for info in infos:
        tags.append(info['tag'])  # 記事カテゴリー
        text = info['text']
        words = doctoword(text)
        data.append(words)  # 形態素解析された単語のベクトル
    return [tags, data]
