import argparse
import os


def split_parallel(file, out1, out2):
    if os.path.exists(out1):
        os.remove(out1)
    if os.path.exists(out2):
        os.remove(out2)

    out_incorr = open(out1, "w")
    out_corr = open(out2, "w")

    with open(file, 'r', encoding='utf-8') as fi:
        for line in fi:
            line = line.strip()
            if line:
                try:
                    orig_sent = line.split('\t')[0]
                    cor_sent = line.split('\t')[1]
                    out_incorr.write(orig_sent + '\n')
                    out_corr.write(cor_sent + '\n')
                except IndexError:
                    print(line)

    out_incorr.close()
    out_corr.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", default="/home/yli/gector/data/BEA_2019/dev_parallel.txt")
    parser.add_argument("-out1", default="/home/yli/gector/data/BEA_2019/dev_incorr.txt")
    parser.add_argument("-out2", default="/home/yli/gector/data/BEA_2019/dev_corr.txt")
    args = parser.parse_args()

    split_parallel(args.file, args.out1, args.out2)
