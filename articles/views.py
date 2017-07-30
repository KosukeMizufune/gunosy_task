from lxml import etree
from django.http import HttpResponseBadRequest
from sklearn.externals import joblib
from django.shortcuts import render
import requests

from utils import doctoword, get_article
from articles.forms import URLForm


# Create your views here.


def urltotag(request):
    """
    入力されたURLからテキストデータを入手し、記事タグを表示させる関数

    :param request: HttpRequest, 入力画面からのリクエスト
    :return: 正当なURLと不正な場合でそれぞれのページに飛ばす
    """
    form = URLForm(request.GET or None)
    target_url = request.POST.get('form')
    try:
        doc = get_article(target_url)
        if not doc:
            tag = "まだURLを未入力、もしくはテキストがないページになっているので分類できませんでした。"
        else:
            words = doctoword(doc)
            nb = joblib.load('naivebayes.cmp')
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
