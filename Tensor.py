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
problem_count = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
problem = [0, 0, 0, 0, 0, 0]
num = 0
leni = [0, 0, 0, 0, 0]
for file in files:
    if file == 'Euc_one2one_pred':
        pred_data = [json.loads(l) for l in open(root_path + '/' + file + '/kp20k.pred', "r")]
        for pred in tqdm.tqdm(pred_data[:10]):
            preds = pred['pred_sents'][:10]
            gds = find_(pred['gold_sent'])
            print('preds=', preds)
            print('gd=', pred['gold_sent'])
            print('+'*50)
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
                    gd_flag = 0
                    gds_flag = 0
                    lens = len(gd)
                    if lens == 0:
                        break
                    if gd in preds:
                        if gd_subphrase is not None:
                            if '<unk>' in gd_subphrase:
                                break
                            for j in range(len(preds)):
                                if gd == preds[j]:
                                    gd_flag = j
                                if gd_subphrase == preds[j]:
                                    gds_flag = j
                            if gd_flag < gds_flag:
                                problem_count[4 if lens > 4 else lens][2] += 1
                                problem[2] += 1
                                print('-'*50)
                                print('gd=', gd, 'gd_subphrase=', gd_subphrase)
                                print('gd in ok and gd_subphrase is in ok too,problem 3++')
                                print('*'*50)
                            else:
                                problem_count[4 if lens > 4 else lens][3] += 1
                                problem[3] += 1
                                print('-' * 50)
                                print('gd=', gd, 'gd_subphrase=', gd_subphrase)
                                print('gd in ok and gd_subphrase is in ok too,problem 4++')
                                print('*' * 50)
                        if gd_superphrase is not None:
                            if '<unk>' in gd_superphrase:
                                break
                            for k in range(len(preds)):
                                if gd == preds[k]:
                                    gd_flag = k
                                if gd_superphrase == preds[k]:
                                    gds_flag = k

                            if gd_flag < gds_flag:
                                problem_count[4 if lens > 4 else lens][4] += 1
                                problem[4] += 1
                                print('-' * 50)
                                print('gd=', gd, 'gd_superphrase=', gd_superphrase)
                                print('gd in ok and gd_superphrase is in ok too,problem 5++')
                                print('*' * 50)
                            else:
                                problem_count[4 if lens > 4 else lens][5] += 1
                                problem[5] += 1
                                print('-' * 50)
                                print('gd=', gd, 'gd_superphrase=', gd_superphrase)
                                print('gd in ok and gd_superphrase is in ok too,problem 6++')
                                print('*' * 50)
                    else:
                        if gd_subphrase is not None:
                            if '<unk>' in gd_subphrase:
                                break
                            problem_count[4 if lens > 4 else lens][0] += 1
                            problem[0] += 1
                            print('-' * 50)
                            print('gd=', gd, 'gd_subphrase=', gd_subphrase)
                            print('gd not in ok and gd_subphrase is in ok,problem 1++')
                            print('*' * 50)
                        if gd_superphrase is not None:
                            if '<unk>' in gd_superphrase:
                                break
                            problem_count[4 if lens > 4 else lens][1] += 1
                            problem[1] += 1
                            print('-' * 50)
                            print('gd=', gd, 'gd_superphrase=', gd_superphrase)
                            print('gd not in ok and gd_superphrase is in ok,problem 2++')
                            print('*' * 50)
print(problem_count[1:])
print(leni[1:])
print(num)
print(problem)
