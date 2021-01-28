def find_superphrase(find_list, target_list):
    for target in target_list:
        if len(target) <= len(find_list):
            break
        temp = creat_ngram(target, len(find_list))
        print(temp)
        for tmp in temp:
            if tmp == find:
                print(target)

def creat_ngram(crate_list, n):
    result = []
    end = len(crate_list)
    if n > end:
        return None
    else:
        for i in range(end - n + 1):
            result.append(crate_list[i:i + n])
        return result


find=['optimization','methods']
target_list = [['asd','optimization', 'methods'], ['123']]
print(find_superphrase(find, target_list))