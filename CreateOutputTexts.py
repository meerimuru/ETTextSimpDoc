import shutil
import json
import os

def create_output_texts(output_dir, articles_json="articles.json"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Copy agents.json into the output directory
    destination = os.path.join(output_dir, "agents.json")
    shutil.copy("agents.json", destination)

    # Load agents.json
    with open("agents.json", "r", encoding="utf-8") as f:
        agents_data = json.load(f)
        agent_keys = list(agents_data["agents"].keys())  # e.g., ["AA", "BB"]

    print(f"Found agents: {agent_keys}")

    # Load articles.json
    with open(articles_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each article and save each agents' output to separate folders
    for entry in data:
        doc_id = entry.get("id", "unknown")
        print(f"\nProcessing article ID: {doc_id}")

        for agent_key in agent_keys:
            content = entry.get(f"{agent_key}")
            if content:
                agent_dir = os.path.join(output_dir, agent_key)
                os.makedirs(agent_dir, exist_ok=True)

                filepath = os.path.join(agent_dir, f"{doc_id}.txt")
                with open(filepath, "w", encoding="utf-8") as out_file:
                    out_file.write(content)
                print(f"Wrote to {filepath}")
            else:
                print(f"No output for {agent_key} in article {doc_id}")

    print(f"\nText files saved in subfolders under: {output_dir}")