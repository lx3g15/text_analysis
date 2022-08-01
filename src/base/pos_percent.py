import sys

input_file = sys.argv[1]

total_words = 0
n_words = 0
ad_words = 0
cp_words = 0

n_pos = ['n',]
ad_pos = ['a','ad','an','d']
cp_pos = ['c','p']
with open(input_file, 'r') as fin:
    for line in fin.readlines():
        word, pos, frq = line.strip().split('\t')
        frq = int(frq)
        total_words += frq
        if pos in n_pos:
            n_words += frq
        elif pos in ad_pos:
            ad_words += frq
        elif pos in cp_pos:
            cp_words += frq

print('总词频:', total_words)
print('名词:', n_words)
print('形副词:', ad_words)
print('介词连词:', cp_words)
