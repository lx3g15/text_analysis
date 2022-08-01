from transformers import BertTokenizer
from transformers import TFAlbertForMaskedLM
import tensorflow as tf
import sys

input_name = sys.argv[1]
input_data = '../../data/'+input_name+'/biwu_info.txt'
output_data = '../../output/'+input_name+'/biwu_result.txt'
tokenizer = BertTokenizer.from_pretrained('./albert_tokenizer/')
model = TFAlbertForMaskedLM.from_pretrained('../../data/'+input_name+'/lm/lm_hugging_face_format')

def parse_score(prediction_score):
    """
    赢 - 6617
    输 - 6783
    胜 - 5526
    败 - 6571
    生 - 4495
    死 - 3647
    活 - 3833
    """
    # logit_prob = tf.keras.layers.Softmax()(prediction_score).numpy()
    logit_prob = prediction_score.numpy()
    total_score = logit_prob[6617] + logit_prob[5526] + logit_prob[4495] + logit_prob[3833] + logit_prob[6783] + logit_prob[6571] + logit_prob[3647]
    # win_score = logit_prob[6617] + logit_prob[5526] + logit_prob[4495] + logit_prob[3833]
    # loss_score = logit_prob[6783] + logit_prob[6571] + logit_prob[3647]
    win_score = logit_prob[6617] + logit_prob[5526]
    loss_score = logit_prob[6783] + logit_prob[6571]
    return win_score, loss_score

def parse_score1(prediction_score):
    """
    胜 - 5526
    利 - 1164
    失 - 1127
    败 - 6571
    """
    logit_prob = prediction_score.numpy()
    win_score = logit_prob[6617] + logit_prob[5526]
    loss_score = logit_prob[6783] + logit_prob[6571]
    return win_score, loss_score

def get_score(inputtext):
    input_ids = tf.constant(tokenizer.encode(inputtext, add_special_tokens=True))[None, :]
    token_ids = tokenizer.encode(inputtext, add_special_tokens=True)
    maskpos_list = list()
    for i in range(len(token_ids)):
        if token_ids[i] == 103:
            maskpos_list.append(i)

    outputs = model(input_ids, labels=input_ids,training = False)
    prediction_scores = outputs[1]

    win_score1, loss_score1 = parse_score(prediction_scores[0, maskpos_list[0]])
    win_score2, loss_score2 = parse_score(prediction_scores[0, maskpos_list[1]])
    person_score1 = win_score1-loss_score1
    person_score2 = win_score2-loss_score2 
    return person_score1, person_score2

def get_score1(inputtext):
    input_ids = tf.constant(tokenizer.encode(inputtext, add_special_tokens=True))[None, :]
    token_ids = tokenizer.encode(inputtext, add_special_tokens=True)
    maskpos_list = list()
    for i in range(len(token_ids)):
        if token_ids[i] == 103:
            maskpos_list.append(i)

    outputs = model(input_ids, labels=input_ids,training = False)
    prediction_scores = outputs[1]

    win_score1, loss_score1 = parse_score1(prediction_scores[0, maskpos_list[0]], prediction_scores[0, maskpos_list[1]])
    win_score2, loss_score2 = parse_score1(prediction_scores[0, maskpos_list[2]], prediction_scores[0, maskpos_list[3]])
    person_score1 = win_score1-loss_score1
    person_score2 = win_score2-loss_score2 
    return person_score1, person_score2

def cal_score(person1_info, person2_info):
    name1, wugong1 = person1_info.split(':')
    name2, wugong2 = person2_info.split(':')
    inputtext1 = name1+'用'+wugong1+'，'+name2+'用'+wugong2+'。'+name1+'[MASK]，'+name2+'[MASK]。'
    first_person_score1, seconde_person_score1 = get_score(inputtext1)
    inputtext2 = name2+'用'+wugong2+'，'+name1+'用'+wugong1+'。'+name2+'[MASK]，'+name1+'[MASK]。'
    second_person_score2, first_person_score2 = get_score(inputtext2)
    first_person_final_score1 = first_person_score1 + first_person_score2
    second_person_final_score1 = seconde_person_score1 + second_person_score2

    inputtext1 = name1+'用'+wugong1+'，'+name2+'用'+wugong2+'。'+name1+'[MASK][MASK]，'+name2+'[MASK][MASK]。'
    first_person_score1, seconde_person_score1 = get_score1(inputtext1)
    inputtext2 = name2+'用'+wugong2+'，'+name1+'用'+wugong1+'。'+name2+'[MASK][MASK]，'+name1+'[MASK][MASK]。'
    second_person_score2, first_person_score2 = get_score1(inputtext2)
    first_person_final_score2 = first_person_score1 + first_person_score2
    second_person_final_score2 = seconde_person_score1 + second_person_score2

print(tokenizer.convert_ids_to_tokens([6617, 6783,5526,6571,4495,3647,3833]))
with open(input_data, 'r') as fin, open(output_data, 'w') as fout:
    for line in fin.readlines():
        items = line.strip().split('\t')
        if len(items) != 2:
            continue
        person1_info, person2_info = items
        name1, wugong1 = person1_info.split(':')
        name2, wugong2 = person2_info.split(':')
        inputtext1 = name1+'用'+wugong1+'，'+name2+'用'+wugong2+'。'+name1+'[MASK]，'+name2+'[MASK]。'
        first_person_score1, seconde_person_score1 = get_score(inputtext1)
        inputtext2 = name2+'用'+wugong2+'，'+name1+'用'+wugong1+'。'+name2+'[MASK]，'+name1+'[MASK]。'
        second_person_score2, first_person_score2 = get_score(inputtext2)
        first_person_final_score = first_person_score1 + first_person_score2
        second_person_final_score = seconde_person_score1 + second_person_score2
        fout.write('{}:{}\t{}:{}\n'.format(name1,first_person_final_score,name2,second_person_final_score))
        print('{}:{}\t{}:{}'.format(name1,first_person_final_score,name2,second_person_final_score))

