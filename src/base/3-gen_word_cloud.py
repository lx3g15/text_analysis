import sys
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import numpy as np

config_file = sys.argv[1]

with open(config_file, 'r') as fin:
    config = json.load(fin)

bg_image_path = config['word_cloud_background']
word_frq_file = config['word_frq_file']
font_path = config['font_path']
wordcloud_output = config['word_cloud_file']
words_frq = dict()

# 读取词频
with open(word_frq_file, 'r') as fin:
    for line in fin.readlines():
        items = line.strip().split('\t')
        if len(items) < 2:
            continue
        word = items[0]
        frq = int(items[-1])
        words_frq[word] = frq

# 词云设置
if bg_image_path is not None:
    # 带背景
    back_coloring = np.array(Image.open(bg_image_path))
    wc = WordCloud(scale=8,font_path=font_path,background_color="white",width=500,height=350,max_words=1000,mask=back_coloring)
else:
    # 不带背景
    wc = WordCloud(scale=8,font_path=font_path,background_color="white",width=500,height=350,max_words=1000)
wc.generate_from_frequencies(words_frq)

# 生成图片
plt.figure()
plt.imshow(wc)
plt.axis("off")
wc.to_file(wordcloud_output)
