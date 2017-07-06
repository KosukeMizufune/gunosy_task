from django.shortcuts import render
from Naivebayes import NaiveBayes
from articleclass.forms import URLForm
from extract import GetArticle
from mecab_article import doctoword
from train_mecab import train_mecab


# Create your views here.


tags, data = train_mecab()

nb = NaiveBayes()
nb.train(tags, data)


def url_list(request):
    form = URLForm(request.GET or None)
    url = request.POST.get('form')
    ar = GetArticle()
    ar.get_article(url)
    article_text = ar.article_text
    if url is None:
        tag = None
    else:
        doc = doctoword(article_text)
        tag = nb.classify(doc)
    f = {
        'form': form,
        'url': url,
        'tag': tag,
    }
    return render(request, 'articleclass/url_list.html', f)
