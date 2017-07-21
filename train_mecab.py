from random import shuffle

from pymongo import MongoClient

from mecab_article import doctoword


# 訓練データをカテゴリーと形態素解析された記事データに分ける関数
def train_mecab():
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
