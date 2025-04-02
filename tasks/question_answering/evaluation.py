import numpy as np
import argparse
import json

def cal_metrics(preds, labels):
    # Accuracy
    accs = []
    for q, pred in zip(labels, preds):
        accs.append(1 if pred == q['answer'] else 0)

    result = {
            'Accuracy': np.array(accs).mean().item()
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