__author__ = 'Long'

from GoogleNews import GoogleNewsParser
from GoogleNews import JsonParser
from Expressions import ExTFIDF
from Expressions import ExD2V
import os
from gensim.models.doc2vec import Doc2Vec
from gensim import corpora
import Algorithm

import sklearn
import gensim

import numpy
from sklearn import metrics

import sys


def main():
    # calculate NMI example
    # results =  [1, 1, 1, 2, 2, 2, 3, 3, 3]
    # clusters = [1, 1, 2, 2, 2, 3, 3, 3, 1]
    # print metrics.adjusted_mutual_info_score(results, clusters)

    # print sys.stdout.encoding
    #Running tfidf
    # parser = GoogleNewsParser.NewsParsers()
    # parser.parse_data_from_tok()

    # tfidf = ExTFIDF.TfIdf()
    # tfidf.fit_data(parser.get_texts())
    # parser.get_texts()
    # print parser.get_texts()
    # JsonParser.get_docs_labels(os.getcwd() + "\\" + "clusters")

    # Running version
    # print "sklearn version: " + sklearn.__version__
    # print "gensim version: " + gensim.__version__

    # running hicocluster
    # run_hicocluster_create_matrix()

    # running TF-IDF
    # algorithm_tfidf()

    # running doc2vec
    run_doc2vec()
    # algorithm with d2v representation
    # algorithm_d2v()
    # GoogleNewsParser.get_target_labels()

    # running combination
    # algorithm_combination()


def run_hicocluster_create_matrix():
    # Number of docs: 1950
    # Number of items: 21826
    texts = JsonParser.get_texts(os.getcwd() + "\\clusters")
    newTexts = []
    for text in texts:
        newTexts.append(text.split())
    # print newTexts[0]

    dictionary = corpora.Dictionary(newTexts)
    dictionary.save(os.getcwd() + "\\dictionary.dict")

    corpus = [dictionary.doc2bow(text) for text in newTexts]
    corpora.MmCorpus.serialize(os.getcwd() + "\\corpus.mm", corpus)
    print "length of docs: " + str(dictionary.num_docs)
    print "length of items: " + str(len(dictionary.token2id.items()))

    features = len(dictionary.token2id.items())
    row = 1
    set_doc_terms = []
    for doc in corpus:
        doc_terms = [0] * features
        if len(doc) > 0:
            row += 1
            for term in doc:
                doc_terms[term[0]] = term[1]
            set_doc_terms.append(doc_terms)
    matrix = open(os.getcwd() + "\\matrix.txt", "w")
    for line in set_doc_terms:
        for i in range(len(line)):
            matrix.write(str(line[i]) + " ")
        matrix.write("\n")
    matrix.close()


def algorithm_tfidf():
    print "Running TFIDF"
    # Google data
    # parser = GoogleNewsParser.NewsParsers()
    # parser.parse_data_from_tok()

    # Json Google
    tfidf = ExTFIDF.TfIdf()
    # tfidf.fit_data(parser.get_texts())
    tfidf.fit_data(JsonParser.get_texts(os.getcwd() + "\\" + "clusters"))

    print "lennth of tfidf : " + str(len(tfidf.get_data_as_vector()))

    print "Running algorithm with TFIDF"
    Algorithm.algorithm_Kmean(tfidf.get_data_as_vector())
    # Algorithm.algorithm_HAC(tfidf.get_data_as_vector())


def algorithm_d2v():
    # load_d2v()
    # Algorithm.algorithm_Kmean(load_d2v())
    Algorithm.algorithm_HAC(load_d2v())


def load_d2v():
    print "load_d2v"
    pairs = []
    module = Doc2Vec.load(os.getcwd() + "\\google.d2v")
    print "length " + str(len(module.docvecs))

    # raw clusters
    # labels = GoogleNewsParser.get_only_labels(os.getcwd() + "\\clusters")

    # json clusters
    labels = JsonParser.get_only_labels(os.getcwd() + "\\clusters")

    docs = []
    for i in range(len(labels)):
        docs.append(module.docvecs[labels[i]])
    pairs.append(labels)
    pairs.append(docs)
    return pairs


def run_doc2vec():
    print "run_doc2vec"
    path = os.getcwd() + "\\clusters"

    # raw clusters
    # pairs = GoogleNewsParser.get_docs_labels(path=path)

    # clusters from json
    pairs = JsonParser.get_docs_labels(path=path)

    documents = ExD2V.DocIterator(pairs[0], pairs[1])
    # model = Doc2Vec(size=100, window=10, min_count=1, workers=4, alpha=0.025, min_alpha=0.025)
    model = Doc2Vec(size=200, window=10, min_count=1, workers=4, alpha=0.025, min_alpha=0.025)
    model.build_vocab(documents)
    for epoch in range(10):
        model.train(documents)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
    print "length of model : " + str(len(model.docvecs))
    model.save(os.getcwd() + "\\google.d2v")


def algorithm_combination():
    final = get_combination()
    Algorithm.algorithm_Kmean(final)
    # Algorithm.algorithm_HAC(final)


def get_combination():
    print "run_combination"
    # Google data
    # parser = GoogleNewsParser.NewsParsers()
    # parser.parse_data_from_tok()

    # Json Google
    tfidf = ExTFIDF.TfIdf()
    # tfidf.fit_data(parser.get_texts())
    tfidf.fit_data(JsonParser.get_texts(os.getcwd() + "\\" + "clusters"))
    tf_vectors = tfidf.get_data_as_vector()
    print "Length of tfidf feature: " + str(len(tf_vectors[0]))
    # print tf_vectors[0]

    pairs = load_d2v()
    single = pairs[1]
    print "Length of doc2vec feature: " + str(len(single[0]))
    # print single[0]

    final = numpy.hstack((tf_vectors, single))
    print "Length of final features: " + str(len(final[0]))
    # final = []
    # for i in range(length):
    #     temp = tf_vectors[i] + single[i]
    #     final.append(temp)
    return final


if __name__ == '__main__':
    main()
