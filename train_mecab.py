from random import shuffle

import MeCab
from pymongo import MongoClient


# 訓練データをカテゴリーと形態素解析された記事データに分ける関数
def train_mecab():
    client = MongoClient('localhost')
    collection = client.scraping.article
    tagger = MeCab.Tagger("-Ochasen -d "
                          "/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    tagger.parse('')
    infos = [x for x in collection.find()]
    shuffle(infos)
    tags = []
    data = []
    for info in infos:
        tokens = []
        tags.append(info['tag'])  # 記事カテゴリー
        text = info['text']
        node = tagger.parseToNode(text)
        while node:
            split = node.feature.split(',')
            category, sub_category = split[:2]
            if category == '名詞' or category == '形容詞' \
                    and sub_category in ('固有名詞', '一般'):
                if split[6] == '*':
                    tokens.append(node.surface)
                else:
                    tokens.append(split[6])
            node = node.next
        data.append(tokens)  # 形態素解析された単語のベクトル
    return [tags, data]
