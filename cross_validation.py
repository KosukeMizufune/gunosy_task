from random import shuffle
import MeCab
from pymongo import MongoClient
from Naivebayes import NaiveBayes

client = MongoClient('localhost')
collection = client.scraping.article
tagger = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
tagger.parse('')
infos = [x for x in collection.find()]
shuffle(infos)
tags= []
data = []
for info in infos:
    tokens = []
    tags.append(info['tag'])
    text = info['text']
    node = tagger.parseToNode(text)
    while node:
        split = node.feature.split(',')
        category, sub_category = split[:2]
        if category =='名詞' or category == '形容詞' and sub_category in ('固有名詞', '一般'):
            if split[6] == '*':
                tokens.append(node.surface)
            else:
                tokens.append(split[6])
        node = node.next
    data.append(tokens)

def cv_accuracy(tags, data, K):
    accuracyList = []
    for n in range(K):  # 各分割について
        # 訓練データとテストデータにわける
        train_data = [d for i, d in enumerate(data) if i % K != n]
        train_tag = [d for i, d in enumerate(tags) if i % K != n]
        test_data = [d for i, d in enumerate(data) if i % K == n]
        test_tag = [d for i, d in enumerate(tags) if i % K == n]
        # ナイーブベイズ分類器を学習
        nb = NaiveBayes()
        nb.train(train_tag, train_data)
        # テストデータの分類精度を計算
        hit = 0
        numTest = 0
        for tag, words in zip(test_tag, test_data):
            predict = nb.classify(words)
            if tag == predict:
                hit += 1
            numTest += 1
        accuracy = float(hit) / float(numTest)
        accuracyList.append(accuracy)
    average = sum(accuracyList) / float(K)
    return(average)

if __name__ == "__main__":
    print(cv_accuracy(tags, data, 5))
