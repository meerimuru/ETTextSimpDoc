import os
import textstat

def eval_FKGL(outputs_dir):
    file_names = sorted([f for f in os.listdir(outputs_dir) if f.endswith(".txt")])

    fkgl_scores = []

    for file_name in file_names:
        with open(os.path.join(outputs_dir, file_name), 'r', encoding='utf-8') as f:
            text = f.read().strip()

        score = textstat.flesch_kincaid_grade(text)
        fkgl_scores.append(score)
        print(f"{file_name}: FKGL = {score:.2f}")

    # Average across documents
    average_fkgl = sum(fkgl_scores) / len(fkgl_scores)
    print(f"\nAverage FKGL across {len(file_names)} documents: {average_fkgl:.2f}")
    return average_fkgl