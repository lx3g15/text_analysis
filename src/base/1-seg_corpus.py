import sys
import json
from LAC import LAC

config_file = sys.argv[1]

print("Load config...")
with open(config_file, 'r') as fin:
    config = json.load(fin)

input_file = config['raw_corpus']
output_file1 = config['seg_corpus']
output_file2 = config['seg_corpus_pos']
custom_dict = config['custom_dict']

print("Start tokenizer...")
lac = LAC(mode = 'lac')
if custom_dict:
    lac.load_customization(custom_dict)

raw_corpus = list()
with open(input_file, 'r') as fin:
    for line in fin.readlines():
        if line.strip():
            raw_corpus.append(line.strip())


with open(output_file1, 'w') as fout1, open(output_file2, 'w') as fout2:
    for line in raw_corpus:
        if line.strip():
            try:
                tokens, pos_list = lac.run(line.strip())
                results = list()
                results_pos = list()
                for i in range(len(tokens)):
                    if not tokens[i].strip():
                        continue
                    results.append(tokens[i])
                    results_pos.append(tokens[i]+'\x01'+pos_list[i])
                if ' '.join(results):
                    fout1.write(' '.join(results)+'\n')
                    fout2.write(' '.join(results_pos)+'\n')
            except:
                print(line.strip())
