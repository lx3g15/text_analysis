#coding=utf-8

import json
import sys
import pprint
from gensim.models import Word2Vec

if __name__ == "__main__":
    config_file = sys.argv[1]
    with open(config_file, 'r') as fin:
        config = json.load(fin)
    corpus_path = config['seg_corpus']
    model_path = config['word2vec_model']
    word = sys.argv[2]

    model = Word2Vec.load(model_path)

    print(word)
    pprint.pprint(model.wv.most_similar(word, topn=50))


