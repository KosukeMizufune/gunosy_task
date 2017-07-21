from collections import defaultdict
import math


# ナイーブベイズを行う関数
class NaiveBayes:
    def __init__(self):
        self.tags_set = set()  # カテゴリの集合
        self.vocabularies_set = set()  # ボキャブラリの集合
        self.wordcount = {}  # wordcount[cat][word] カテゴリでの単語の出現回数
        self.tagcount = {}  # catcount[cat] カテゴリの出現回数
        self.denominator = {}  # denominator[cat] P(word|cat)の分母の値

    # 分類するのに必要なパラメータを計算する関数
    def train(self, tags, data):
        for tag in tags:
            self.tags_set.add(tag)
        for tag in self.tags_set:
            self.wordcount[tag] = defaultdict(int)
            self.tagcount[tag] = 0
        for (tag, d) in zip(tags, data):
            self.tagcount[tag] += 1
            for word in d:
                self.vocabularies_set.add(word)
                self.wordcount[tag][word] += 1
        for tag in self.tags_set:
            self.denominator[tag] = \
                sum(self.wordcount[tag].values()) + len(self.vocabularies_set)

    # 未知の記事データからカテゴリを分類する関数
    def classify(self, doc):
        best = None
        top = -float('inf')
        for tag in self.tagcount.keys():
            p = self.score(doc, tag)
            if p >= top:
                top = p
                best = tag
        return best

    # 各カテゴリーの各単語の生起確率を計算
    def word_prob(self, word, tag):
        return (self.wordcount[tag][word] + 1) / self.denominator[tag]

    # 対数尤度関数
    def score(self, doc, tag):
        total = sum(self.tagcount.values())
        score = math.log(float(self.tagcount[tag]) / total)
        for word in doc:
            score += math.log(self.word_prob(word, tag))
        return score
