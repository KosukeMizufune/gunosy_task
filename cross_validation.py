from Naivebayes import NaiveBayes
from train_mecab import train_mecab


# 分類器に対して交差検証する関数


tags, data = train_mecab()


def cv_accuracy(tags, data, k):
    accuracylist = []
    for n in range(k):  # 各分割について
        # 訓練データとテストデータにわける
        train_data = [d for i, d in enumerate(data) if i % k != n]
        train_tag = [d for i, d in enumerate(tags) if i % k != n]
        test_data = [d for i, d in enumerate(data) if i % k == n]
        test_tag = [d for i, d in enumerate(tags) if i % k == n]
        # ナイーブベイズ分類器を学習
        nb = NaiveBayes()
        nb.train(train_tag, train_data)
        # テストデータの分類精度を計算
        hit = 0
        numtest = 0
        for tag, words in zip(test_tag, test_data):
            predict = nb.classify(words)
            if tag == predict:
                hit += 1
            numtest += 1
        accuracy = float(hit) / float(numtest)
        accuracylist.append(accuracy)
    average = sum(accuracylist) / float(k)
    return average

if __name__ == "__main__":
    print(cv_accuracy(tags, data, 5))
