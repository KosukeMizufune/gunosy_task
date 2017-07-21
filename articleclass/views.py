from lxml import etree
from django.http import HttpResponseBadRequest
from django.shortcuts import render
import requests

from mecab_article import doctoword
from extract import get_article
from naivebayes import NaiveBayes
from train_mecab import train_mecab
from articleclass.forms import URLForm


# Create your views here.

tags, data = train_mecab()
nb = NaiveBayes()
nb.train(tags, data)


def urltotag(request):
    form = URLForm(request.GET or None)
    target_url = request.POST.get('form')
    try:
        doc = get_article(target_url)
        if not doc:
            tag = "まだURLを未入力、もしくはテキストがないページになっているので分類できませんでした。"
        else:
            words = doctoword(doc)
            tag = nb.classify(words)
        f = {
            'form': form,
            'url': target_url,
            'tag': tag,
        }
        return render(request, 'articleclass/urltotag.html', f)
    except etree.XMLSyntaxError:
        return HttpResponseBadRequest(
            '<h1>URLが間違っています。Gunosyの記事URLを入力してください</h1>')
    except requests.ConnectionError:
        return HttpResponseBadRequest(
            '<h1>URLが不正です。Gunosyの記事URLを入力してください</h1>')
