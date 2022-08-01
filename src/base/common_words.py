import sys

input_file = sys.argv[1]

words1 = set()
words2 = set()
words3 = set()
words4 = set()
words5 = set()
with open(input_file, 'r') as fin:
    for line in fin.readlines():
        #word1, word2, word3, word4, word5 = line.strip().split('\t')
        word1, word2, word3 = line.strip().split('\t')
        words1.add(word1)
        words2.add(word2)
        words3.add(word3)
        #words4.add(word4)
        #words5.add(word5)

#same_words = words1 & words2 & words3 & words4 & words5
same_words = words1 & words2 & words3
print(same_words)
