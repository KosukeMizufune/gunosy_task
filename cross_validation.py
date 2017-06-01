from Naivebayes import NaiveBayes
from train_mecab import train_MeCab

#分類器に対して交差検証する関数

tags, data = train_MeCab()

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
