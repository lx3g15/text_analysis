import json
import sys
from collections import defaultdict


if __name__ == "__main__":
    config_file = sys.argv[1]

    with open(config_file, 'r') as fin:
        config = json.load(fin)


    stop_word_file = config['stop_word_dict']
    input_file = config['seg_corpus_pos']
    output_unigram = config['unigram_file']
    output_bigram = config['bigram_file']
    output_trigram = config['trigram_file']

    stop_words = set()
    unigram_frq = defaultdict(int)
    bigram_frq = defaultdict(int)
    trigram_frq = defaultdict(int)

    with open(stop_word_file, 'r') as fin:
        for line in fin.readlines():
            stop_words.add(line.strip().split('\t')[0])

    with open(input_file, 'r') as fin:
        for line in fin.readlines():
            words_info = line.strip().split()
            for i in range(len(words_info)):
                if len(words_info[i].split('\x01')) !=2:
                    continue
                word, pos = words_info[i].split('\x01')
                if word in stop_words:
                    continue
                # unigram
                unigram_frq[word+'\t'+pos] += 1
                #if len(word) >1:
                #    unigram_frq[word+'\t'+pos] += 1
                # bigram
                if i < len(words_info)-1:
                    if len(words_info[i+1].split('\x01')) !=2:
                        continue
                    bigram_word, bigram_pos = words_info[i+1].split('\x01')
                    if bigram_word in stop_words:
                        continue
                    bigram_frq[word+bigram_word+'\t'+pos+'|'+bigram_pos] += 1
                # trigram
                if i < len(words_info)-2:
                    if len(words_info[i+2].split('\x01')) !=2:
                        continue
                    trigram_word, trigram_pos = words_info[i+2].split('\x01')
                    if trigram_word in stop_words:
                        continue
                    trigram_frq[word+bigram_word+trigram_word+'\t'+pos+'|'+bigram_pos+'|'+trigram_pos] += 1

    order_unigram = sorted(unigram_frq.items(), key = lambda x:x[1], reverse=True)
    order_bigram = sorted(bigram_frq.items(), key = lambda x:x[1], reverse=True)
    order_trigram = sorted(trigram_frq.items(), key = lambda x:x[1], reverse=True)

    with open(output_unigram, 'w') as fout:
        for word, frq in order_unigram:
            fout.write(word+'\t'+str(frq)+'\n')
    with open(output_bigram, 'w') as fout:
        for word, frq in order_bigram:
            fout.write(word+'\t'+str(frq)+'\n')
    with open(output_trigram, 'w') as fout:
        for word, frq in order_trigram:
            fout.write(word+'\t'+str(frq)+'\n')


    word_frq_file = output_unigram[:-4]+'_no_pos.txt'
    with open(output_unigram, 'r') as fout, open(word_frq_file, 'w') as fin:
        word_frq_dict = defaultdict(int)
        for line in fout.readlines():
            word, _, frq = line.strip().split('\t')
            frq = int(frq)
            word_frq_dict[word] += frq
        order_word_frq = sorted(word_frq_dict.items(), key = lambda x:x[1], reverse=True)
        for word, frq in order_word_frq:
            fin.write(word+'\t'+str(frq)+'\n')
