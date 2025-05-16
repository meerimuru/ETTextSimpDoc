from SinglePass import single_pass
from CreateOutputTexts import create_output_texts
from PipelineOnly import pipeline
from PipelineGuideline import pipeline_guideline

if __name__ == "__main__":
    models = ["meta-llama/llama-3.3-70b-instruct", "openai/gpt-4.1", "google/gemini-2.0-flash-001"]

    for model in models:
        model_name = model.split("/")[-1]

        # Single-Pass
        prompts_dir_single = "./Prompts/SinglePass"
        single_pass(prompts_dir_single, model)

        output_dir_single = f"./output_texts/{model_name}/SinglePass"
        create_output_texts(output_dir_single)

        # Pipeline-Only
        prompts_dir_pipeline = "./Prompts/Pipeline"
        pipeline_order = ["TI", "SS", "AA"]
        pipeline(prompts_dir_pipeline, pipeline_order, model)

        output_dir_pipeline = f"./output_texts/{model_name}/Pipeline"
        create_output_texts(output_dir_pipeline)

        # Pipeline-Guideline
        prompts_dir_pipeline_guideline = "./Prompts/PipelineGuideline"
        pipeline_guideline_order = ["PD", "TI", "SS", "AA"]
        pipeline_guideline(prompts_dir_pipeline_guideline, pipeline_guideline_order, model)

        output_dir_pipeline = "./output_texts/{model_name}/PipelineGuideline"
        create_output_texts(output_dir_pipeline)