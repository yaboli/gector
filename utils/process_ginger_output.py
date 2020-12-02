import pandas as pd
import argparse
import os


def write_to_file(iterable, path):
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as fo:
        for x in iterable:
            if x.strip():
                fo.write(x + '\n')


def is_nan(cell):
    return pd.isna(cell)


def main():
    file_path = args.file
    prefix = file_path.split('/')[-1][:-4]
    prefix = prefix.replace(' ', '_')

    ext = '.txt'
    out_dir = '/home/yli/gector/data/ginger'
    out1 = os.path.join(out_dir, prefix + '_original' + ext)
    out2 = os.path.join(out_dir, prefix + '_expected' + ext)
    out3 = os.path.join(out_dir, prefix + '_corrected' + ext)

    original_sentences = []
    expected_sentences = []
    corrected_sentences = []

    df = pd.read_csv(file_path)
    prev_id = -1
    original_sentence = []
    expected_sentence = []
    corrected_sentence = []

    for _, row in df.iterrows():
        sentence_id = row['Sentence ID']

        if is_nan(sentence_id):
            break

        original_sequence = str(row['Original Sequence'])
        expected_sequence = str(row['Expected Sequence'])
        corrected_sequence = str(row['Corrected Sequence'])

        if sentence_id != prev_id:
            original_sentences.append(' '.join(original_sentence))
            expected_sentences.append(' '.join(expected_sentence))
            corrected_sentences.append(' '.join(corrected_sentence))
            original_sentence.clear()
            expected_sentence.clear()
            corrected_sentence.clear()
            prev_id = sentence_id

        original_sentence.append(original_sequence)
        expected_sentence.append(expected_sequence)
        corrected_sentence.append(corrected_sequence)

    if original_sentence:
        original_sentences.append(' '.join(original_sentence))
        expected_sentences.append(' '.join(expected_sentence))
        corrected_sentences.append(' '.join(corrected_sentence))

    assert len(original_sentences) == len(expected_sentences) and len(original_sentences) == len(corrected_sentences)

    write_to_file(original_sentences, out1)
    write_to_file(expected_sentences, out2)
    write_to_file(corrected_sentences, out3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-file",
                        default="/home/yli/gector/data/ginger/outputs for simon/tester and user feedback_output.csv")
    args = parser.parse_args()
    main()
