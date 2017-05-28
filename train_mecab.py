from pymongo import MongoClient
import MeCab
from random import shuffle

def train_MeCab():
    client = MongoClient('localhost')
    collection = client.scraping.article
    tagger = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    tagger.parse('')
    infos = [x for x in collection.find()]
    shuffle(infos)
    tags = []
    data = []
    for info in infos:
        tokens = []
        tags.append(info['tag'])
        text = info['text']
        node = tagger.parseToNode(text)
        while node:
            split = node.feature.split(',')
            category, sub_category = split[:2]
            if category == '名詞' or category == '形容詞' and sub_category in ('固有名詞', '一般'):
                if split[6] == '*':
                    tokens.append(node.surface)
                else:
                    tokens.append(split[6])
            node = node.next
        data.append(tokens)
    return([tags, data])