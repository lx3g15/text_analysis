#coding=utf-8

import json
import sys
from gensim.models import word2vec
import logging


if __name__ == "__main__":
    config_file = sys.argv[1]
    with open(config_file, 'r') as fin:
        config = json.load(fin)
    corpus_path = config['seg_corpus']
    model_save_path = config['word2vec_model']
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    print("reading corpus...")
    corpus = word2vec.LineSentence(corpus_path)
    print("training model...")
    model = word2vec.Word2Vec(corpus, hs=1,min_count=5,window=10,size=50, workers=4, iter=10, sg=0)
    print("saving model...")
    model.save(model_save_path)
