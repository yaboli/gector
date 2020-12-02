import random


def merge(filenames, out_path):
    with open(out_path, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line)


def merge_and_shuffle(filenames, out_path, seed=123):
    random.seed(seed)
    data = []
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                if line.strip():
                    data.append((random.random(), line))
    data.sort()
    with open(out_path, 'w') as outfile:
        for _, line in data:
            outfile.write(line)


if __name__ == '__main__':
    FILE_NAMES = [
        '/home/yli/gector/data/BEA_2019/lang8/train_parallel.txt',
        '/home/yli/gector/data/BEA_2019/fce/train_parallel.txt',
        '/home/yli/gector/data/BEA_2019/fce/dev_parallel.txt',
        '/home/yli/gector/data/BEA_2019/fce/test_parallel.txt',
        '/home/yli/gector/data/BEA_2019/wi+locness/train_parallel.txt',
        '/home/yli/gector/data/BEA_2019/nucle/train_parallel.txt'
    ]
    OUT_PATH = '/home/yli/gector/data/BEA_2019/merged_parallel.txt'

    merge_and_shuffle(FILE_NAMES, OUT_PATH)

    # FILE_NAMES = [
    #     '/home/yli/gec-docs/synthetic/a1/a1_train_incorr_sentences.txt',
    #     '/home/yli/gector/data/ginger/synthetic/newsgcca-en-fr.en.train/incorr_sentences.txt'
    # ]
    # OUT_PATH = '/home/yli/gector/data/ginger/synthetic/merged/incorr_sentences.txt'
    #
    # merge(FILE_NAMES, OUT_PATH)
