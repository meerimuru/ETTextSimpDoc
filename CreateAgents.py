import os
import json

def create_agents(input_folder, output_json_path="agents.json"):
    # Dictionary to hold agent data
    agents_dict = {}

    # Loop over all .txt files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            agent_code = filename.replace(".txt", "").strip()

            filepath = os.path.join(input_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    continue  # Skip empty files

                name = lines[0].strip()
                # Skips the first line in txt files as it's the name of the agent
                description = "".join(lines[1:]).strip()

                agents_dict[agent_code] = {
                    "name": name,
                    "task_description": description
                }

    output_data = {
        "agents": agents_dict
    }

    # Save to JSON file
    with open(output_json_path, "w", encoding="utf-8") as out_file:
        json.dump(output_data, out_file, indent=2, ensure_ascii=False)

    print(f"Agent data written to: {output_json_path}")