import MeCab


# URLから入手した記事を形態素解析する関数
def doctoword(doc):
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
