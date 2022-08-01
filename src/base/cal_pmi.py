import sys
import re
import math
from collections import defaultdict

if __name__ == "__main__":
    raw_corpus = sys.argv[1]
    unigram_file = sys.argv[2]
    stop_word_file = sys.argv[3]

    total_unigram = 0
    unigram_frq = dict()
    with open(unigram_file, 'r') as fin:
        for line in fin.readlines():
            word, frq = line.strip().split('\t')
            frq = int(frq)
            total_unigram += frq
            unigram_frq[word] = frq
    print(unigram_frq['周翡'])

    """
    for k,v in unigram_frq.items():
        unigram_frq[k] = v/total_unigram
    """

    stop_words = set()
    with open(stop_word_file, 'r') as fin:
        for line in fin.readlines():
            stop_words.add(line.strip().split('\t')[0])

    bigram_frq = defaultdict(int)
    with open(raw_corpus, 'r') as fin:
        for line in fin.readlines():
            if '周翡' not in line:
                continue
            line = re.sub('[。？！]', '###', line)
            sentences = line.strip().split('###')
            for sentence in sentences:
                if  '周翡' not in sentence:
                    continue
                words = sentence.strip().split()
                words = [word for word in words if len(word) > 1]
                target_index = words.index('周翡')
                # 每一行里的全部算共现
                for i in range(len(words)):
                    if words[i] in stop_words:
                        continue
                    if target_index == i:
                        continue
                    bigram_frq[words[i]] += 1
            """
            for i in range(-3,4):
                if i==0:
                    continue
                j = target_index + i
                if j >=0 and j<len(words):
                    bigram_frq[words[j]] += 1
            """

    pmi = dict()
    for k,v in bigram_frq.items():
        if v <=5:
            continue
        if len(k) >1:
            pmi[k] = v*math.log2(v/unigram_frq['周翡']/unigram_frq[k])

    pmi = sorted(pmi.items(), key = lambda x:x[1], reverse=True)
    with open('pmi.output', 'w') as fout:
        for word, pmi_value in pmi:
            fout.write(word+'\t'+str(pmi_value)+'\n')
