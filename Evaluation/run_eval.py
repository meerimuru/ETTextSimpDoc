from Eval_BERTS import eval_BERTS
from Eval_DSARI import eval_DSARI
from Eval_FKGL import eval_FKGL
import os
import csv

def save_scores(scores_dict, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Load existing scores if the file exists
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            rows = list(reader)
    else:
        # Initialize header and empty score rows
        rows = [["metric"] + list(scores_dict.keys())]
        for metric in ["fkgl", "berts", "dsari"]:
            rows.append([metric] + [""] * len(scores_dict))

    # Update the scores
    for col_index, system_name in enumerate(scores_dict, start=1):  # skip 'metric' column
        for row in rows:
            if row[0] in scores_dict[system_name]:
                # Extend row if needed
                while len(row) <= col_index:
                    row.append("")
                row[col_index] = f"{scores_dict[system_name][row[0]]:.4f}"

    # Write scores
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    print(f"\nSaved scores to: {output_file}")

if __name__ == "__main__":
    # === folder paths ===
    originals_dir = "data/originals"
    references_dir = "data/references"
    model_dirs = ["data/Gemini-2.0-flash-001", "data/GPT-4.1", "data/LLama-3.3-70b-Instruct"]

    for model_dir in model_dirs:
        outputs_dirs = [f"{model_dir}/SinglePass", f"{model_dir}/PipelineOnly", f"{model_dir}/PipelineGuideline"]

        all_scores = {}

        for dir in outputs_dirs:
            system_name = os.path.basename(dir)

            print(f"\n=== Evaluating {system_name} ===")

            fkgl_score = eval_FKGL(dir)
            print(f"  FKGL:     {fkgl_score:.4f}")

            bertscore = eval_BERTS(dir, references_dir)
            print(f"  BERTScore:{bertscore:.4f}")

            dsari_score = eval_DSARI(originals_dir, dir, references_dir)
            print(f"  D-SARI:   {dsari_score:.4f}")

            all_scores[system_name] = {
                "fkgl": fkgl_score,
                "berts": bertscore,
                "dsari": dsari_score
            }

            # Save all to a single TSV
        scores_path = os.path.join(model_dir, "scores.tsv")
        save_scores(all_scores, scores_path)