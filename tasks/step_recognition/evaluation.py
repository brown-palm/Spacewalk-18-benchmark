import numpy as np
import argparse
import json

steps = json.load(open('../../data/steps.json'))
n_labels = {date: len(v) for date, v in steps.items()}

def mAP(prob, label):
    prs = [(0, 0), (1, 0)] # (recall, precision)
    L = list(zip(prob, label))
    L.sort(reverse=True, key=lambda x: (x[0], -x[1]))
    M = sum(label)
    TP = 0
    FP = 0
    for p, l in L:
        if l == 1:
            TP += 1
        else:
            FP += 1
        prs.append((TP / M, TP / (TP + FP)))
    prs.sort(reverse=True)
    n = len(prs)
    ret = 0.0
    mx = prs[0][1]
    for i in range(1, n):
        ret += (prs[i-1][0] - prs[i][0]) * mx
        mx = max(mx, prs[i][1])
    return ret

def cal_metrics(pred, labels):
    # mAP
    if 'score' in pred[list(pred.keys())[0]][0]:
        mAP_ = []
        for date in pred:
            tmp = []
            for i in range(1, n_labels[date]):
                tmp.append(mAP(
                    [x['score'][i] for x in pred[date]],
                    [1 if x['label'] == i else 0 for x in labels[date]]
                ))
            mAP_.append(np.mean(tmp))
        mAP_ = np.mean(mAP_)
    else:
        mAP_ = 'N/A'

    # Accuracy
    accs = []
    for date in pred:
        prediction = np.array([x['prediction'] for x in pred[date]])
        label = np.array([x['label'] for x in labels[date]])
        n_label = n_labels[date]
        # Confusion Matrix
        A = np.zeros((n_label, n_label))
        for i in range(len(label)):
            A[label[i], prediction[i]] += 1
        # Accuracy
        acc = np.diag(A).sum() / A.sum()
        accs.append(acc)

    result = {
            'Accuracy': np.array(accs).mean(),
            'mAP': mAP_
        }

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", type=str)
    parser.add_argument("--gt", type=str)
    args = parser.parse_args()
    print(cal_metrics(
        json.load(open(args.pred)),
        json.load(open(args.gt))
    ))