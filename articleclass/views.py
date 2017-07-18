from django.shortcuts import render

from mecab_article import doctoword
from extract import get_article
from Naivebayes import NaiveBayes
from train_mecab import train_mecab
from articleclass.forms import URLForm


# Create your views here.

tags, data = train_mecab()
nb = NaiveBayes()
nb.train(tags, data)


def url_list(request):
    form = URLForm(request.GET or None)
    target_url = request.POST.get('form')
    article_text = get_article(target_url)
    if target_url is None:
        tag = None
    else:
        doc = doctoword(article_text)
        tag = nb.classify(doc)
    f = {
        'form': form,
        'url': target_url,
        'tag': tag,
    }
    return render(request, 'articleclass/url_list.html', f)
