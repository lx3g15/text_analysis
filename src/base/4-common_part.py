import sys
import re

if __name__ == "__main__":
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]

    corpus1 = set()
    corpus2 = set()

    with open(input_file1, 'r') as fin:
        for line in fin.readlines():
            new_line = re.sub('[，。！？]', '<n>', line.strip())
            new_line = re.sub('[“”]', '', new_line)
            sentences = new_line.split('<n>')
            for sentence in sentences:
                corpus1.add(sentence)

    with open(input_file2, 'r') as fin:
        for line in fin.readlines():
            new_line = re.sub('[，。！？]', '<n>', line.strip())
            new_line = re.sub('[“”]', '', new_line)
            sentences = new_line.split('<n>')
            for sentence in sentences:
                corpus2.add(sentence)

    same_corpus = corpus1 & corpus2
    with open('same_corpus.txt', 'w') as fout:
        for sentence in same_corpus:
            if len(sentence) > 3:
                fout.write(sentence+'\n')
