import random
import argparse


def split_file(file, out1, out2, percentage=0.75, shuffle=True, seed=123):
    """Splits a file in 2 given the `percentage` to go in the large file."""
    random.seed(seed)
    with open(file, 'r', encoding="utf-8") as fin, \
            open(out1, 'w') as foutBig, \
            open(out2, 'w') as foutSmall:
        nLines = sum(1 for line in fin)
        fin.seek(0)

        nTrain = int(nLines * percentage)
        nValid = nLines - nTrain

        i = 0
        for line in fin:
            r = random.random() if shuffle else 0  # so that always evaluated to true when not isShuffle
            if (i < nTrain and r < percentage) or (nLines - i > nValid):
                foutBig.write(line)
                i += 1
            else:
                foutSmall.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='/home/yli/gec-docs/synthetic/a1/a1_train_corr_sentences.txt')
    parser.add_argument('--out1', default='/home/yli/gec-docs/synthetic/a6/a6_train_corr_sentences.txt')
    parser.add_argument('--out2', default='/home/yli/gec-docs/synthetic/a6/a6_dev_corr_sentences.txt')
    args = parser.parse_args()

    split_file(args.file, args.out1, args.out2, percentage=0.98)
