import os
import json
from openai import OpenAI
from CreateAgents import create_agents

def pipeline_guideline(
    prompts_dir,
    pipeline_order,
    model,
    input_folder="Articles",
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

    # Process each article file
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            article_id = os.path.splitext(filename)[0]
            with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                lines = f.readlines()
                original_text = "".join(lines[1:]).strip()

            article_entry = {
                "id": article_id,
                "original_text": original_text
            }

            # PD: generate guideline from original text
            pd_task = agents["PD"]["task_description"]
            pd_prompt = (f"{pd_task}\n\n"
                         f"Document:\n{original_text}")
            pd_response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": pd_prompt}]
            )
            pd_output = pd_response.choices[0].message.content
            article_entry["PD"] = pd_output

            # Set up for pipeline
            current_input = original_text

            # Remaining pipeline: TI → SS → AA
            for agent_key in pipeline_order[1:]:
                # Skips the first line in txt files as they're metadata lines
                task_description = agents[agent_key]["task_description"]
                prompt = (
                    f"{task_description}\n\n"
                    f"Guidelines:\n{pd_output}\n\n"
                    f"Document:\n{current_input}"
                )

                response = openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )

                output = response.choices[0].message.content
                article_entry[f"{agent_key}"] = output
                current_input = output  # Pass to next agent

            output_articles.append(article_entry)

    # Save to output_file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_articles, f, ensure_ascii=False, indent=2)

    print(f"\nSaved articles to: {output_file}")