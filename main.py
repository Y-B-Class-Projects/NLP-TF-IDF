import datetime
import util
import math
from tabulate import tabulate
import os
from collections import Counter
import numpy as np
from scipy import spatial
from tqdm import tqdm


def make_dictionary(file):
    words = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            words += line.split()
    return words


def main():
    docs_files = ['data\\' + file for file in os.listdir('data') if file.endswith(".txt")]
    query_files = ['query\\' + file for file in os.listdir('query') if file.endswith(".txt")]
    all_files = docs_files[:10000] + query_files

    all_words = []
    for file in tqdm(all_files):
        all_words += make_dictionary(file)
    all_words = Counter(all_words).most_common()

    count_words = []
    for word in tqdm(all_words):
        if word[1] > 111 and len(word[0]) > 1 and word[0] not in util.get_stop_words():
            count_words += [[word[0], word[1]]]
    print("Total words", len(count_words))

    tf = []
    for file in tqdm(all_files):
        file_list = []
        file_words = make_dictionary(file)
        for word in count_words:
            file_list += [file_words.count(word[0])]
        tf.append({'file': file, 'words': file_list})
    print("done tf")

    df = []
    for word_index in tqdm(range(len(count_words))):
        df.append(sum([1 for doc in tf if doc['words'][word_index] >= 1]))
    print("done df")

    m = len(tf)
    idf = [math.log((m + 1) / df_i, 10) for df_i in df]
    print("done idf")

    tf_idf = []
    for tf_doc in tqdm(tf):
        value = np.multiply(tf_doc['words'], idf)
        tf_idf.append({'file': tf_doc['file'], 'value': value})
    print("done tf-idf")

    cosine_distances = []
    euclidean_distances = []
    for doc in tqdm(tf_idf[:-1]):
        cosine_distances.append([doc['file'], spatial.distance.cosine(list(tf_idf[-1]['value']), list(doc['value']))])
        euclidean_distances.append([doc['file'], spatial.distance.euclidean(list(tf_idf[-1]['value']), list(doc['value']))])

    cosine_distances = sorted(cosine_distances, key=lambda x: x[1])
    cosine_distances = [it for it in cosine_distances if it[1] != 0]
    euclidean_distances = sorted(euclidean_distances, key=lambda x: x[1])

    print(tabulate(cosine_distances[:10], headers=['file','cosine distances'], tablefmt='fancy_grid'))
    print(tabulate(euclidean_distances[:10], headers=['file','euclidean distances'], tablefmt='fancy_grid'))


if __name__ == '__main__':
    tic = datetime.datetime.now()
    main()
    toc = datetime.datetime.now()
    print((toc - tic))
