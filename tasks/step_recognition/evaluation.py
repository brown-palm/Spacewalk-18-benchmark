import numpy as np
import argparse
import json

steps = json.load(open('../../data/steps.json'))
annotations = json.load(open('../../data/annotation.json'))
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

def list_to_intervals(preds):
    res = {}
    for date in preds:
        ST = annotations[date][1]['frame_start']
        ED = annotations[date][-2]['frame_end']
        for i, pred in enumerate(preds[date]):
            if i == 0:
                res[date] = [{
                    'frame_start': ST,
                    'frame_end': (pred['frame_index'] + preds[date][i+1]['frame_index']) / 2,
                    'pred': pred['prediction']
                }]
            elif i + 1 == len(preds[date]):
                res[date].append({
                    'frame_start': (pred['frame_index'] + preds[date][i-1]['frame_index']) / 2,
                    'frame_end': ED,
                    'pred': pred['prediction']
                })
            else:
                res[date].append({
                    'frame_start': (pred['frame_index'] + preds[date][i-1]['frame_index']) / 2,
                    'frame_end': (pred['frame_index'] + preds[date][i+1]['frame_index']) / 2,
                    'pred': pred['prediction']
                })
    return res

def IoU(preds, labels):
    for date in preds:
        assert len(preds[date]) == len(labels[date])
        for i in range(len(preds[date])):
            preds[date][i]['frame_index'] = labels[date][i]['frame_index']
    preds = list_to_intervals(preds)

    IoU_per_date = []
    for date in preds:
        n_steps = max([x['label'] for x in annotations[date]]) + 1
        IoUs = []
        for step_id in range(n_steps):
            gt_len = 0
            for seg in annotations[date]:
                if seg['label'] == step_id:
                    gt_len += seg['frame_end'] - seg['frame_start']
            pred_len = 0
            for seg in preds[date]:
                if seg['pred'] == step_id:
                    pred_len += seg['frame_end'] - seg['frame_start']
            intersection = 0
            for seg in annotations[date]:
                if seg['label'] != step_id: continue
                for pred in preds[date]:
                    if pred['pred'] != step_id: continue
                    if pred['frame_end'] < seg['frame_start'] or pred['frame_start'] > seg['frame_end']:
                        continue
                    L = max(pred['frame_start'], seg['frame_start'])
                    R = min(pred['frame_end'], seg['frame_end'])
                    intersection += R - L
            IoUs.append(intersection / (gt_len + pred_len - intersection))
        IoU_per_date.append(np.mean(IoUs))
    IoU_ = np.mean(IoU_per_date).item()

    return IoU_

def cal_metrics(pred, labels):
    # IoU
    IoU_ = IoU(pred, labels)

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
        mAP_ = np.mean(mAP_).item()
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
            'Accuracy': np.array(accs).mean().item(),
            'mAP': mAP_,
            'IoU': IoU_
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