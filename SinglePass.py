from openai import OpenAI
import json
import os
from CreateAgents import create_agents

def single_pass(
    prompts_dir,
    model,
    input_dir="Articles",
    output_file="articles.json"
):

    # Set OpenAI API key and model
    api_key = ""
    openai_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,)

    # Create agents from prompts
    create_agents(prompts_dir)

    # Load agent task descriptions
    with open("agents.json", "r", encoding="utf-8") as f:
        agents_data = json.load(f)
        agents = agents_data["agents"]

    output_articles = []

    # Iterates over all the articles in input_dir
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            article_id = os.path.splitext(filename)[0]
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Skips the first line in txt files as they're metadata lines
                original_text = "".join(lines[1:]).strip()

            # Saves original text to json
            article_entry = {
                "id": article_id,
                "original_text": original_text
            }

            agent_key = "SPS"
            task_description = agents[agent_key]["task_description"]
            prompt = (
                f"{task_description}\n\n"
                f"Document:\n{original_text}"
            )

            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            # Saves response
            output = response.choices[0].message.content
            article_entry[f"{agent_key}"] = output

            output_articles.append(article_entry)

    # Save to output_file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_articles, f, ensure_ascii=False, indent=2)

    print(f"\nSaved articles to: {output_file}")