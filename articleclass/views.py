import urllib.error

from django.shortcuts import render
from django.http import HttpResponseBadRequest

from mecab_article import doctoword
from extract import get_article
from Naivebayes import NaiveBayes
from train_mecab import train_mecab
from articleclass.forms import URLForm


# Create your views here.

tags, data = train_mecab()
nb = NaiveBayes()
nb.train(tags, data)


def urltotag(request):
    form = URLForm(request.GET or None)
    target_url = request.POST.get('form')
    tag = None
    if not target_url:
        pass
    elif urllib.error.HTTPError:
        return HttpResponseBadRequest('<h1>分類するページは見つかりません</h1>')
    else:
        doc = get_article(target_url)
        if not doc:
            tag = "こちらのURLにはテキストは存在しないので分類できませんでした。テキストがあるかどうかをお確かめください。"
        else:
            words = doctoword(doc)
            tag = nb.classify(words)
    f = {
        'form': form,
        'url': target_url,
        'tag': tag,
    }
    return render(request, 'articleclass/url_list.html', f)
