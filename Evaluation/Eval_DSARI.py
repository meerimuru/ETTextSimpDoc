import os
import numpy as np
from D_SARI import D_SARIsent


def read_file(path):
    # Reads in a file
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def eval_DSARI(originals_dir, outputs_dir, references_dir):
    # A list to store the original articles
    files = sorted(os.listdir(originals_dir))
    scores = []

    # Iterates over all of the files
    for file in files:
        orig_path = os.path.join(originals_dir, file)
        out_path = os.path.join(outputs_dir, file)
        ref_path = os.path.join(references_dir, file)

        orig_text = read_file(orig_path)
        out_text = read_file(out_path)
        ref_text = read_file(ref_path)

        # Calculates D-SARI
        sari_score = D_SARIsent(orig_text, out_text, [ref_text])
        scores.append(sari_score)

        print(f"{file}: D-SARI = {(sari_score[0]):.4f}")

    # Calculates the avarage of the scores
    avg = np.mean(scores)
    print(f"\nAverage D-SARI across {len(scores)} documents: {avg:.4f}")
    return avg

if __name__ == "__main__":
    originals_dir = "data/originals"
    outputs_dir = "data/system_outputs"
    references_dir = "data/references"

    eval_DSARI(originals_dir, outputs_dir, references_dir)