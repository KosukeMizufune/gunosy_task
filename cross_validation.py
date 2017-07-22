from naivebayes import NaiveBayes
from train_mecab import train_mecab


def cv_accuracy(tags, data, k):
    """
    分類器に対してk交差検証する関数

    :param tags: list, 記事のタグ
    :param data: list, 記事のテキストデータ
    :param k: int, k交差検証のk
    :return: float, k交差検証で計算されたaccuracyの平均値
    """
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
        accuracy = hit / numtest
        accuracylist.append(accuracy)
    average = sum(accuracylist) / k
    return average

if __name__ == "__main__":
    tags, data = train_mecab()
    print(cv_accuracy(tags, data, 5))
