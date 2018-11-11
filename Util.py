
def find_candidates(items1, items2):
    result = []
    for i in range(len(items1)):
        if items1[i] in items2:
            result.append(i)
    return result


def one_hot(labels, label_id, label_num):
    result = []
    for i in range(0, len(labels)):
        one_hot_vec = [0] * label_num
        one_hot_vec[label_id[labels[i]]] = 1
        result.append(one_hot_vec)
    return result