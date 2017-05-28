import MeCab
from django.shortcuts import render
from pymongo import MongoClient
from Naivebayes import NaiveBayes
from articleclass.forms import URLForm
from extract import article
from mecab_article import doctoword

# Create your views here.


client = MongoClient('localhost')
collection = client.scraping.article
tagger = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
tagger.parse('')
infos = [x for x in collection.find()]
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

nb = NaiveBayes()
nb.train(tags, data)


def url_list(request):
    form = URLForm(request.GET or None)
    url = request.POST.get('form')
    ar = article()
    ar.get_article(url)
    article_text = ar.article_text
    doc = doctoword(article_text)
    tag = nb.classify(doc)
    if article_text is None:
        article_text = "urlを入力してください"
    f = {
        'form': form,
        'url': url,
        'tag': tag,
    }
    return render(request, 'articleclass/url_list.html', f)


