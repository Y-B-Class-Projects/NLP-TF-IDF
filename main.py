import collections
import datetime

from gensim.similarities.docsim import query_shard

import util
import math
from tabulate import tabulate
import os
from collections import Counter
import numpy as np
from scipy import spatial
from tqdm import tqdm
import textwrap
import pandas as pd


def make_dictionary(file):
    words = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            words += line.split()
    return words


def calculateTF(wordset, bow, avdl):
    b = 0.75
    termfreq_diz = dict.fromkeys(wordset, 0)
    counter1 = dict(collections.Counter(bow))
    for w in bow:
        termfreq_diz[w] = counter1[w] / ((1 - b) + b * len(bow) / avdl)
    return termfreq_diz


def calculate_IDF(wordset, bow):
    d_bow = {'bow_{}'.format(i): list(set(b)) for i, b in enumerate(bow)}
    N = len(d_bow.keys())
    l_bow = []
    for b in d_bow.values():
        l_bow += b
    counter = dict(collections.Counter(l_bow))
    idf_diz = dict.fromkeys(wordset, 0)
    for w in wordset:
        idf_diz[w] = np.log((1 + N) / (1 + counter[w])) + 1
    return idf_diz


def calculate_TF_IDF(wordset, tf_diz, idf_diz):
    tf_idf_diz = dict.fromkeys(wordset, 0)
    for w in wordset:
        tf_idf_diz[w] = tf_diz[w] * idf_diz[w]
    tdidf_values = list(tf_idf_diz.values())
    return tdidf_values


def main():
    query_str = "ליאונל מסי"
    docs_files = ['data\\' + file for file in os.listdir('data') if file.endswith(".txt")]
    #query_files = ['query\\' + file for file in os.listdir('query') if file.endswith(".txt")]
    all_files = docs_files[1:1000]

    files_words = {}
    for file in tqdm(all_files):
        files_words[file] = make_dictionary(file)
    files_words["Query"] = query_str.split()

    all_words = query_str.split()
    for file in tqdm(all_files):
        all_words += make_dictionary(file)
    all_words = Counter(all_words).most_common()

    all_words_temp = []
    for word in tqdm(all_words):
        if word[1] > 5 and len(word[0]) > 1 and word[0] not in util.get_stop_words():
            all_words_temp += [word[0]]
    all_words = all_words_temp
    #print(all_words)

    avdl = np.average([len(bow) for bow in list(files_words.values())])

    IDF = calculate_IDF(all_words, list(files_words.values()))
    #print(IDF)

    cosine_distances = []
    euclidean_distances = []
    query_TF_IDF = calculate_TF_IDF(all_words, calculateTF(all_words, list(files_words.get("Query")), avdl), IDF)
    for file in tqdm(files_words):
        if file != "Query":
            doc_TF_IDF = calculate_TF_IDF(all_words, calculateTF(all_words, files_words[file], avdl), IDF)
            cosine_distances.append([file, spatial.distance.cosine(query_TF_IDF, doc_TF_IDF)])
            euclidean_distances.append([file, spatial.distance.euclidean(query_TF_IDF, doc_TF_IDF)])


    cosine_distances = sorted(cosine_distances, key=lambda x: x[1])
    cosine_distances = [it for it in cosine_distances if it[1] != 0]
    euclidean_distances = sorted(euclidean_distances, key=lambda x: x[1])
    euclidean_distances = [it for it in euclidean_distances if it[1] != 0]

    print(tabulate(cosine_distances[:10], headers=['file', 'cosine distances'], tablefmt='fancy_grid'))
    print(tabulate(euclidean_distances[:10], headers=['file', 'euclidean distances'], tablefmt='fancy_grid'))

    print(cosine_distances[0][0], ":")
    with open(cosine_distances[0][0], 'r', encoding='utf-8') as f:
        for line in f:
            print('\n'.join(textwrap.wrap(line, 100, break_long_words=False)))
    print(euclidean_distances[0][0], ":")
    with open(euclidean_distances[0][0], 'r', encoding='utf-8') as f:
       for line in f:
           print('\n'.join(textwrap.wrap(line, 100, break_long_words=False)))


if __name__ == '__main__':
    tic = datetime.datetime.now()
    main()
    toc = datetime.datetime.now()
    print('\n' + str((toc - tic)))
