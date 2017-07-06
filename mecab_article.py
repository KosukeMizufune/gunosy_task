import MeCab


# URLから入手した記事データを形態素解析する関数
def doctoword(article):
    tagger = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    tagger.parse('')
    node = tagger.parseToNode(article)
    tokens = []
    while node:
        split = node.feature.split(',')
        category, sub_category = split[:2]  # 品詞情報
        if category == '名詞' or category == '形容詞' and sub_category in ('固有名詞', '一般'):
            if split[6] == '*':
                tokens.append(node.surface)
            else:
                tokens.append(split[6])
        node = node.next
    return tokens
