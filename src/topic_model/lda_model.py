from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import joblib
import sys

stop_words_file = sys.argv[1]
file_path = sys.argv[2]

# 打印每个主题的top词
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
            for i in topic.argsort()[:-n_top_words - 1:-1]]))
    #print(model.components_)

# 读取语料
def load_corpus(file_path):
    doc = ''
    corpus = list()
    with open(file_path, 'r') as fin:
        for line in fin.readlines():
            if not line.strip():
                continue
            if line.startswith('☆'):
                if doc:
                    corpus.append(doc)
                doc = ''
            else:
                doc = doc + ' ' + line.strip()
        if doc:
            corpus.append(doc)
    return corpus

# 读取停用词
stop_words = list()
with open(stop_words_file, 'r') as fin:
    for line in fin.readlines():
        stop_words.append(line.strip())

# 读取语料
corpus = load_corpus(file_path)

# countVectorizer
cntVector = CountVectorizer(stop_words=stop_words)
cntTf = cntVector.fit_transform(corpus)
joblib.dump(cntVector, './youfei_vectorizer.model')

# lda模型
lda = LatentDirichletAllocation(n_components=10,learning_offset=50.,random_state=0,max_iter=20)
docres = lda.fit_transform(cntTf)
for item in docres:
    max_score = 0
    max_index = -1
    for index, score in enumerate(item):
        if score > max_score:
            max_index = index
            max_score = score
    print(max_index)
#print(docres)
joblib.dump(lda, './youfei_lda.model')

# 展示top n结果
tf_feature_names = cntVector.get_feature_names()
print_top_words(lda, tf_feature_names, 20)
