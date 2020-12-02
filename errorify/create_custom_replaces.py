import pandas as pd
from nltk.corpus import words
import pickle
import argparse
import os


def is_word(s):
    return s in words.words()


def is_nan(cell):
    return pd.isna(cell)


def create_custom_replace(path):
    df = pd.read_csv(path)
    replace_dic = dict()
    consistency_map = {
        'often': 100,
        'sometimes': 10
    }
    for _, row in df.iterrows():
        consistency = row['corrections consistency']
        if consistency in {'often', 'sometimes'}:
            ws = []
            for i in range(4):
                cell = row['word' + str(i + 1)]
                if not is_nan(cell):
                    ws.append(cell)
            l = len(ws)
            for i in range(l):
                wi = ws[i]
                if is_word(wi):
                    if wi not in replace_dic:
                        replace_dic[wi] = dict()
                    dic = replace_dic[wi]
                    for j in range(l):
                        if j != i:
                            dic[ws[j]] = consistency_map[consistency]

    if os.path.exists(args.output):
        os.remove(args.output)

    pickle.dump(replace_dic, open(args.output, "wb"))


def main():
    create_custom_replace(args.input)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", default="/home/yli/gector/data/ginger/confused_words_list.csv")
    parser.add_argument("-output", default="/home/yli/gector/errorify/custom/replaces.p")
    args = parser.parse_args()
    main()
