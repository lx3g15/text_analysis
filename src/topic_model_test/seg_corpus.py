import sys
import json
from LAC import LAC


input_file = sys.argv[1]
output_file1 = sys.argv[2]

print("Start tokenizer...")
lac = LAC(mode = 'lac')

raw_corpus = list()
with open(input_file, 'r') as fin:
    for line in fin.readlines():
        if line.strip():
            raw_corpus.append(line.strip())


with open(output_file1, 'w') as fout1:
    for line in raw_corpus:
        if line.strip():
            try:
                tokens, pos_list = lac.run(line.strip())
                results = list()
                for i in range(len(tokens)):
                    if not tokens[i].strip():
                        continue
                    results.append(tokens[i])
                if ' '.join(results):
                    fout1.write(' '.join(results)+' ')
            except:
                print(line.strip())
    fout1.write('\n')
