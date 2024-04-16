import numpy as np
import argparse
import json

def cal_metrics(pred, labels):
    # Accuracy
    accs = []
    for date in pred:
        prediction = np.array(pred[date])
        label = np.array([x['label'] for x in labels[date]])
        acc = (prediction == label).sum() / len(label)
        accs.append(acc)

    result = {
            'Accuracy': np.array(accs).mean()
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