import os
pred_result = r'C:\Users\2333\Desktop\yty\抽取结果\KDD\keyphrase.txt'
gold_path = r'C:\Users\2333\Desktop\yty\真实关键词\KDD\gold'

with open(r'C:\Users\2333\Desktop\yty\KDD_filelist', 'r') as f:
    text = f.readline()
    text = text.split(',')
    print(text)
    result = open(pred_result, 'r')
    print(result.readline())
    for path in text:
        f = open(os.path.join(gold_path, path), 'r')
        print(f.readlines())
