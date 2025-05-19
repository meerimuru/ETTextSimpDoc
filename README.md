# Document-Level Text Simplification in Estonian Using Large Language Models

This repository accompanies the bachelor's thesis Document-Level Text Simplification in Estonian Using Large Language Models. It includes all relevant code used for prompt execution, agent configuration, and output evaluation. The aim of this project is to evaluate how well large language models can perform document-level text simplification in Estonian, a low-resource language, and to compare the effectiveness of single-pass prompting versus two types of multi-agent prompting frameworks.

## Overview
**Language**: Estonian

**Models evaluated**:
* GPT-4.1
* LLaMA-3.3
* Gemini-2.0  

**Prompting strategies**:  
* Single-Pass
* Pipeline-Only
* Pipeline-Guideline

The simplification is performed on a set of 15 Estonian Wikipedia articles, and evaluated using BERT-S, D-SARI, and FKGL.

## Repository Structure
📁**Evaluation/**  
Contains evaluation scripts, data and automatic metric outputs.  
&nbsp;&nbsp;&nbsp;&nbsp;📁**Data/**  
&nbsp;&nbsp;&nbsp;&nbsp;Contains data used to automatically evaluate model outputs and model outputs. Organized by model and strategy.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📁**originals/**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains the original articles used in the experiments.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📁**references/**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains manually simplified versions of the articles used as reference outputs.  
📁**Prompts/**  
Contains prompt templates for each method. Organized by method.  
&nbsp;&nbsp;&nbsp;&nbsp;📁**Pipeline/**  
&nbsp;&nbsp;&nbsp;&nbsp;📁**PipelineGuideline/**  
&nbsp;&nbsp;&nbsp;&nbsp;📁**SinglePass/**  

## Main Scripts
``` CreateAgents.py ``` – Generates agent configurations and updates agents.json

``` CreateOutputTexts.py ``` – Compiles outputs by agent and strategy

``` FetchRandArticles.py ``` – Randomly selects 15 documents for simplification, based on criteria

``` PipelineOnly.py ``` – Runs multi-agent pipeline (no guideline variant)

``` PipelineGuideline.py ``` – Runs multi-agent pipeline with a guideline agent

``` SinglePass.py ``` – Runs a single-pass simplification prompt

``` run_agents.py ``` – Main script that queries OpenRouter with the constructed prompts and chosen models

## Evaluation scripts  
```D_SARI.py``` ([from Document-Level Text Simplification: Dataset, Criteria and Baseline's GitHub](https://github.com/RLSNLP/Document-level-text-simplification/blob/main/D_SARI.py))  
```Eval_BERTS.py```  ([utilizing the bert_score package](https://github.com/Tiiiger/bert_score))  
```Eval_DSARI.py```  
```Eval_FKGL.py```  ([utilizing the textstat package](https://github.com/textstat/textstat))  
```run_eval.py``` – Runs all evaluations and generates scores.tsv for each model

## JSON Files  
``` agents.json ``` – Configuration file with agent descriptions  
``` articles.json ``` – Contains article ID, original text and agents' outputs  

## Models Used  
All models were accessed via the [OpenRouter](https://openrouter.ai/) platform.  
```openai/gpt-4.1```  
```meta-llama/llama-3-70b-instruct```  
```google/gemini-2.0-flash-001```  

