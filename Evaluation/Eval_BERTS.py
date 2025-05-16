import os
from bert_score import score
import logging
import transformers
transformers.tokenization_utils.logger.setLevel(logging.ERROR)
transformers.configuration_utils.logger.setLevel(logging.ERROR)
transformers.modeling_utils.logger.setLevel(logging.ERROR)

def eval_BERTS(references_dir, outputs_dir, model_type="xlm-roberta-large"):
    # === Load and match files ===
    file_names = sorted([
        f for f in os.listdir(outputs_dir)
        if f.endswith(".txt") and os.path.exists(os.path.join(references_dir, f))
    ])

    # === Read contents ===
    candidates = []
    references = []
    used_files = []

    for file_name in file_names:
        with open(os.path.join(outputs_dir, file_name), "r", encoding="utf-8") as f_out:
            system_text = f_out.read().strip()

        with open(os.path.join(references_dir, file_name), "r", encoding="utf-8") as f_ref:
            reference_text = f_ref.read().strip()

        if system_text and reference_text:
            candidates.append(system_text)
            references.append(reference_text)
            used_files.append(file_name)

    # === Compute BERTScore ===
    print(f"Computing BERTScore for {len(candidates)} documents using model: {model_type}")
    P, R, F1 = score(
        candidates,
        references,
        model_type=model_type,  # Optional if model is language-agnostic (like XLM-R)
        verbose=True
    )

    # === Output Results ===
    for i, fname in enumerate(used_files):
        print(f"{fname}: BERTScore F1 = {F1[i].item():.4f}")

    print(f"\nAverage BERTScore F1: {F1.mean().item():.4f}")
    return F1.mean().item()