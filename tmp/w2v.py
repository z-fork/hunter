# -*- coding: utf-8 -*-

import logging

from gensim import corpora, models, similarities, matutils


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)


documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]


stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

print texts

all_tokens = sum(texts, [])

print all_tokens

tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

texts = [[word for word in text if word not in tokens_once]
         for text in texts]

print texts

dictionary = corpora.Dictionary(texts)
print dictionary

print dictionary.token2id

corpus = [dictionary.doc2bow(text) for text in texts]

print corpus

# tfidf = models.TfidfModel(corpus)
#
# corpus_tfidf = tfidf[corpus]
#
# for doc in corpus_tfidf:
#     print doc
#
# new_doc = "Human computer interaction"
# new_vec = dictionary.doc2bow(new_doc.lower().split())
# print new_vec
#
# index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=14)
# sims = index[tfidf[new_vec]]
# print list(enumerate(sims))
#
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# lsiout = lsi.print_topic(2)
# print lsiout

matrix = matutils.corpus2csc(corpus)

print matrix
