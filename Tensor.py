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
                    return gram
    return None


def find_superphrase(find_list, target_list):
    for target in target_list:
        if len(target) <= len(find_list):
            break
        temp = creat_ngram(target, len(find_list))
        for tmp in temp:
            if tmp == find_list:
                return target
    return None


def creat_ngram(crate_list, n):
    result = []
    end = len(crate_list)
    if n > end:
        return None
    else:
        for i in range(end - n + 1):
            result.append(crate_list[i:i + n])
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
problem_count = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
num = 0
leni = [0, 0, 0, 0, 0]
for file in files:
    if file == 'Euc_one2one_pred':
        pred_data = [json.loads(l) for l in open(root_path + '/' + file + '/kp20k.pred', "r")]
        for pred in tqdm.tqdm(pred_data):
            preds = pred['pred_sents'][:10]
            gds = find_(pred['gold_sent'])
            num += len(gds)
            for i in range(1, 5):
                gd_subphrase = []
                gd_superphrase = []
                pred_subphrase = []
                pred_superphrase = []
                leni[i] += len(gds[i])
                for gd in gds[i]:
                    gd_subphrase = find_subphrase(gd, preds)
                    gd_superphrase = find_superphrase(gd, preds)
                    lens = len(gd)
                    if gd in preds:
                        if gd_subphrase is not None:
                            if '<unk>' in gd_subphrase:
                                break
                            # print('-'*10)
                            # print(gd, gd_subphrase)
                            # print('*'*10)
                            problem_count[4 if lens > 4 else lens][2] += 1
                        if gd_superphrase is not None:
                            if '<unk>' in gd_superphrase:
                                break
                            # print('-' * 10)
                            # print(gd, gd_superphrase)
                            # print(preds)
                            # print('*' * 10)
                            problem_count[4 if lens > 4 else lens][3] += 1
                    else:
                        if gd_subphrase is not None:
                            if '<unk>' in gd_subphrase:
                                break
                            print('-' * 10)
                            print(gd, gd_subphrase)
                            print(preds)
                            print('+' * 10)
                            problem_count[4 if lens > 4 else lens][0] += 1
                        if gd_superphrase is not None:
                            if '<unk>' in gd_superphrase:
                                break
                            problem_count[4 if lens > 4 else lens][1] += 1
print(problem_count[1:])
print(leni[1:])
print(num)
