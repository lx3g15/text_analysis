from transformers import AlbertConfig, TFAlbertForMaskedLM, TFAlbertModel
import sys

file_path = sys.argv[1]

# 保存TFAlbertModel
"""
print('reading config...')
config = AlbertConfig.from_json_file('./albert_zh/albert_config.json')
print('loading model...')
model = TFAlbertModel.from_pretrained('./albert_zh/albert_pytorch_model.bin', from_pt=True, config=config)
print('saving model...')
model.save_pretrained('./albert_hugging_face_zh')
"""

# 保存TFAlbertForMaskedLM
config = AlbertConfig.from_json_file(file_path+'/albert_config.json')
model = TFAlbertForMaskedLM.from_pretrained(file_path+'/albert_pytorch_model.bin', from_pt=True, config=config)
model.save_pretrained(file_path+'./lm_hugging_face_format')

