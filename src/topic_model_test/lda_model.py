from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import joblib
import sys

stop_words_file = sys.argv[1]

# 打印每个主题的top词
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
            for i in topic.argsort()[:-n_top_words - 1:-1]]))
    #print(model.components_)

# 读取停用词
stop_words = list()
with open(stop_words_file, 'r') as fin:
    for line in fin.readlines():
        stop_words.append(line.strip())

# 读取语料
doc_list = ['1.output', '2.output', '3.output', '4.output', '5.output']
corpus = list()
for doc in doc_list:
    with open(doc, 'r') as fout:
        corpus.append(fout.read())

# countVectorizer
cntVector = CountVectorizer(stop_words=stop_words)
cntTf = cntVector.fit_transform(corpus)
joblib.dump(cntVector, './vectorizer_sklearn.model')

# lda模型
lda = LatentDirichletAllocation(n_components=7,learning_offset=50.,random_state=0,max_iter=100)
docres = lda.fit_transform(cntTf)
joblib.dump(lda, './LDA_sklearn_main.model')
print(docres)

# 展示top n结果
tf_feature_names = cntVector.get_feature_names()
print_top_words(lda, tf_feature_names, 10)
