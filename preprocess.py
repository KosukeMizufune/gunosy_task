from gensim import matutils, models
import numpy as np


def make_bow(data, dictionary, corpus=None, tfidf=None):
    if corpus is None:
        num_terms = len(dictionary)
        num_doc = len(data)
        bow = np.zeros((num_doc, num_terms))
        for k, d in enumerate(data):
            corpus = dictionary.doc2bow(d)
            bow[k, :] = list(
                matutils.corpus2dense([corpus], num_terms=num_terms)[:, 0])
    else:
        if tfidf is False:
            num_terms = len(corpus[0])
        else:
            num_terms = len(dictionary)
        num_doc = len(data)
        bow = np.zeros((num_doc, num_terms))
        for k, corp in enumerate(corpus):
            bow[k, :] = list(
                matutils.corpus2dense([corp], num_terms=num_terms)[:, 0])
    return bow


def tf_idf(corpus):
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return corpus_tfidf


def tf_idf_bow(data, dictionary):
    corpus = [dictionary.doc2bow(d) for d in data]
    corpus_tfidf = tf_idf(corpus)
    bow = make_bow(data, dictionary, corpus=corpus_tfidf, tfidf=True)
    return bow


def lsi_bow(data, dictionary, num_topics, tfidf=None):
    corpus = [dictionary.doc2bow(d) for d in data]
    if tfidf is not None:
        corpus = tf_idf(corpus)
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
    corpus_lsi = lsi[corpus]
    bow = make_bow(data, dictionary, corpus_lsi)
    return bow
