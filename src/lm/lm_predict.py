from transformers import BertTokenizer
from transformers import TFAlbertForMaskedLM
import tensorflow as tf
import sys

input_name = sys.argv[1]
tokenizer = BertTokenizer.from_pretrained('./albert_tokenizer/')
model = TFAlbertForMaskedLM.from_pretrained(input_name+'/lm_hugging_face_format')

name = "段誉"
inputtext = '萧峰一记降龙十八掌打在'+name+'胸口，'+name+'[MASK]了。'
#inputtext = '南海鳄神一掌打在'+name+'胸口，'+name+'[MASK][MASK]了。'
input_ids = tf.constant(tokenizer.encode(inputtext, add_special_tokens=True))[None, :]
token_ids = tokenizer.encode(inputtext, add_special_tokens=True)
maskpos_list = list()
for i in range(len(token_ids)):
    if token_ids[i] == 103:
        maskpos_list.append(i)

outputs = model(input_ids, labels=input_ids,training = False)
prediction_scores = outputs[1]

predictions = list()
for maskpos in maskpos_list:
    logit_prob = tf.keras.layers.Softmax()(prediction_scores[0, maskpos]).numpy()
    predicted_index = tf.argmax(prediction_scores[0, maskpos])
    predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
    predictions.append(predicted_token)
    print(predicted_token,logit_prob[predicted_index])

print(inputtext)
seg_inputtext = tokenizer.tokenize(inputtext)
i = 0
predicted_text = ''
for word in seg_inputtext:
    if word == '[MASK]':
        predicted_text += predictions[i]
        i += 1
    else:
        predicted_text += word
print(predicted_text)
