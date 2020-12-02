import argparse
import utils.toolbox as toolbox
from tqdm import tqdm
import os


def process_chunks(chunks):
    orig = list()
    corr = list()
    for i in tqdm(range(len(chunks))):
        info = chunks[i]
        # Get the original and corrected sentence + edits for each annotator.
        orig_sent, coder_dict = toolbox.processM2(info)
        orig_sent = ' '.join(orig_sent)
        orig.append(orig_sent)
        # Save info about types of edit groups seen
        if coder_dict:
            annotations = list()
            # Loop through the annotators
            for coder, coder_info in sorted(coder_dict.items()):
                cor_sent = ' '.join(coder_info[0])
                annotations.append(cor_sent)
            corr.append('\t'.join(annotations))
        else:
            # If no error found, save original sentence to corr list
            corr.append(orig_sent)
    return orig, corr


def m2_to_parallel(m2, out):

    if os.path.exists(out):
        os.remove(out)

    # Setup output m2 file
    out_parallel = open(out, "w")

    print("Processing files...")
    # Open the m2 file and split into sentence+edit chunks.
    m2_file = open(m2).read().strip().split("\n\n")
    orig, corr = process_chunks(m2_file)
    for orig_sent, corr_sent in zip(orig, corr):
        out_parallel.write(orig_sent + '\t' + corr_sent + '\n')

    out_parallel.close()


if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser(description="Filter an M2 file based on edits in a reference M2 file (both generated with identical settings with ERRANT).")
    parser.add_argument("-m2", help="The M2 file.", required=True)
    parser.add_argument("-out", help="The output filepath to the parallel file.", required=True)
    args = parser.parse_args()

    m2_to_parallel(args.m2, args.out)
