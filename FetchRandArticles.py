import os
import random
import shutil

# Selects random articles out of a directory, based on word count and desired sample size
def select_random_articles(source_dir, target_dir, min_word_length, max_word_length, sample_size, encoding="utf-8"):
    os.makedirs(target_dir, exist_ok=True)
    eligible_files = []

    for filename in os.listdir(source_dir):
        if filename.endswith(".txt"):
            full_path = os.path.join(source_dir, filename)
            with open(full_path, "r", encoding=encoding) as f:
                lines = f.readlines()
                if len(lines) > 1:
                    content = " ".join(lines[1:])  # Skip first line
                    word_count = len(content.split())
                    if min_word_length <= word_count <= max_word_length:
                        eligible_files.append(filename)

    print(f"Found {len(eligible_files)} eligible files ({min_word_length}–{max_word_length} words).")

    selected_files = random.sample(eligible_files, sample_size)

    for filename in selected_files:
        shutil.copy(
            os.path.join(source_dir, filename),
            os.path.join(target_dir, filename)
        )

    print(f"Copied {sample_size} files to {target_dir}.")

# === Example usage ===
if __name__ == "__main__":
    select_random_articles(
        source_dir="",
        target_dir="",
        min_word_length=50,
        max_word_length=250,
        sample_size=15
    )
