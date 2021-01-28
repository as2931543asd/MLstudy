import json
import tqdm
import os


def find_subphrase(find_list, target_list):
    for j in range(len(find_list)):
        ngram = creat_ngram(find_list, j + 1)
        for gram in ngram:
            if gram in target_list:
                if find_list == gram:
                    pass
                else:
                    # print('phrase=', find_list)
                    # print('subphrase is be found subphrase=', gram)
                    return gram
    return None


def find_superphrase(find_list, target_list):
    count = 0
    superphrase = []
    for find in find_list:
        for target in target_list:
            if len(find_list) >= len(target):
                return None
            else:
                for i in range(len(target)):
                    if find == target[i]:
                        count += 1
                        superphrase = target
    if count == len(find_list):
        if find_list == superphrase:
            pass
        else:
            return superphrase
    else:
        return None


def creat_ngram(crate_list, n):
    result = []
    end = len(crate_list)
    if n > end:
        return None
    else:
        for i in range(end-n+1):
            result.append(crate_list[i:i+n])
        return result


def find_(gen_list):
    result = [[], [], [], [], []]
    for x in gen_list:
        x_len = len(x)
        if x_len == 1:
            result[1].append(x)
        elif x_len == 2:
            result[2].append(x)
        elif x_len == 3:
            result[3].append(x)
        else:
            result[4].append(x)
    return result
        

root_path = r'D:\statistics_hyper_kpg'
files = os.listdir(root_path)
problem_count = [0, 0, 0, 0]
num=0
for file in files:
    if file == 'Euc_one2seq_pred':
        pred_data = [json.loads(l) for l in open(root_path + '/' + file + '/kp20k.pred', "r")]
        for pred in tqdm.tqdm(pred_data):
            gd_subphrase = []
            gd_superphrase = []
            pred_subphrase = []
            pred_superphrase = []
            num += len(pred['gold_sent'])
            for sent in pred['pred_sents']:
                pred_subphrase = find_subphrase(sent, pred['gold_sent'])
                pred_superphrase = find_superphrase(sent, pred['gold_sent'])
                if sent in pred['gold_sent']:
                    if pred_subphrase in pred['gold_sent']:
                        problem_count[2] += 1
                    if pred_superphrase in pred['gold_sent']:
                        problem_count[3] += 1
                else:
                    if pred_subphrase in pred['gold_sent']:
                        problem_count[0] += 1
                    if pred_superphrase in pred['gold_sent']:
                        problem_count[1] += 1
            for gd in pred['gold_sent']:
                gd_subphrase = find_subphrase(gd, pred['pred_sents'])
                gd_superphrase = find_superphrase(gd, pred['pred_sents'])
                if gd in pred['pred_sents']:
                    if gd_subphrase in pred['pred_sents']:
                        problem_count[3] += 1
                    if gd_superphrase in pred['pred_sents']:
                        problem_count[2] += 1
                else:
                    if gd_subphrase in pred['pred_sents']:
                        problem_count[1] += 1
                    if gd_superphrase in pred['pred_sents']:
                        problem_count[0] += 1
                        print('---------------------')
                        print(gd, gd_superphrase)
                        print('---------------------')

print(problem_count)
print(num)
