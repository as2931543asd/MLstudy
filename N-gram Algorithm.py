import spacy
import json
import tqdm
import os
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
# import numpy as np
import pandas

spacy_en = spacy.load('en_core_web_sm')


def tokenize_en(text):
    """
    Tokenizes English text from a string into a list of strings (tokens)
    """
    return [tok.text for tok in spacy_en.tokenizer(text)]


# n-gram-list
def create_ngram(input_list, ngram_num):
    ngram_list = []
    input_list = tokenize_en(input_list)
    if len(input_list) <= ngram_num:
        ngram_list.append(input_list)
    else:
        for tmp in zip(*[input_list[i:] for i in range(ngram_num)]):
            tmp = " ".join(tmp)
            ngram_list.append(tmp)

    return ngram_list   # list,set


def find_subphrase(keyphrase, text):
    """
    Args:
    kephrase (list):the list of reference key phrase
    text (str):the result of model generation
    if want to find the superphrase,
    let para:keyphrase=your:model_generation
        para:model_generation=your:keyphrase
    """
    result = []
    for i in range(1, len(tokenize_en(text))):
        text_ngram = create_ngram(text, i)
        for phrase in text_ngram:
            if phrase in keyphrase:
                print('text=', text)
                print('subphrase=', phrase)
                result.append(phrase)
    return result


def transfer(keyword_list):
    result = []
    for keyword in keyword_list:
        keyword = keyword.lower().replace('-', '') if keyword.find('-') else keyword.lower()
        result.append(keyword)
    return result


def statistics(keyphrase, model_generation):
    keyphrase = transfer(keyphrase)
    model_generation = transfer(model_generation)
    short_generation = 0
    long_generation = 0
    duplicate_generation = 0
    for keyword in model_generation:
        lens = len(find_subphrase(keyphrase, keyword))
        if keyword in keyphrase:
            if lens > 0:
                duplicate_generation += 1
                print('duplicate_generation')
        else:
            if lens > 0:
                long_generation += 1
                print('long_generation')
    for keyword in keyphrase:
        lens=len(find_subphrase(model_generation, keyword))
        if keyword in model_generation:
            if lens > 0:
                duplicate_generation += 1
                print('duplicate_generation')
        else:
            if lens > 0:
                short_generation += 1
                print('short_generation')

    return short_generation, long_generation, duplicate_generation


if __name__ == "__main__":
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    root_path = r'D:\statistics_hyper_kpg'
    files = os.listdir(root_path)
    label = []
    short_generation = 0
    long_generation = 0
    duplicate_generation = 0
    generation_num = 0
    count = 0
    problem_count = 0
    reference_num = 0
    for file in files:
        if file == 'Euc_one2seq_catseq_pred':
            print('start processing: ' + file)
            label.append(file)
            pred_data = [json.loads(l) for l in open(root_path + '/' + file + '/kp20k.pred', "r")]
            for pred in tqdm.tqdm(pred_data):
                count += 1
                keyphrase = []
                generation = []
                for gd in pred['gold_sent']:
                    result = ''
                    for text in gd:
                        result += ' ' + text
                    result = result[1:]
                    keyphrase.append(result)
                reference_num+=len(keyphrase)
                for sent in pred['pred_sents']:
                    result = ''
                    for text in sent:
                        result += ' ' + text
                    result = result[1:]
                    generation.append(result)
                generation_num += len(generation)

                short_temp, long_temp, duplicate_temp = statistics(keyphrase, generation)
                if short_temp != 0:
                    short_generation += short_temp

                if long_temp != 0:
                    long_generation += long_temp
                if duplicate_temp != 0:
                    duplicate_generation += duplicate_temp
                if short_temp!=0 or long_temp!=0 or duplicate_temp!=0:
                    problem_count+=1

    print('------------------------------------')
    print('Total '+str(count)+' times generation')
    print('generation '+str(generation_num)+' keyphrase')
    print('reference number=',reference_num)
    print('short_generation=', short_generation)
    print('long_generation=', long_generation)
    print('duplicate_generation=', duplicate_generation)
    print('problem_count=', problem_count)
