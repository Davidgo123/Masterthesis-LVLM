## 1. Project Structure

### 1.1. datasets
This Projects includes data from the datatset news400 [link](https://data.uni-hannover.de/dataset/tamperednews-news400-ijmir21), tamperedNews [link](https://data.uni-hannover.de/dataset/tamperednews-news400-ijmir21) and mmg [link](https://link.springer.com/chapter/10.1007/978-3-031-28238-6_14).
Each Dataset contains all used images, the used samples (news400_merged.jsonl, tamperednews.json and test_dataset.json) and the entity mapping data.

### 1.2. experiments
each experiment contains his own generated questions from the datasets and script to analize the answers.
1. experiments without comparative images 
    1. document verification
    2. entity verification
2. with comparative images (single image input models)
    1. entity verification with single image
    2. entity verificaiton with multiple images
3. with comparative images (multi image input models)
    1. entity verification with single image
    2. entity verificaiton with multiple images

### 1.3. model_scripts
Each model requiered different options to generate answers and probailities.
Mantis and Deepseek requiered additional ressources:
- [mantis](https://github.com/TIGER-AI-Lab/Mantis)
- [deepseek](https://github.com/deepseek-ai/DeepSeek-VL)
After download, the scripts (mantis.py and deepseek.py) need to be moved in the downloaded ressource

### 1.4. used vision language models
- [blip-2-7b](https://huggingface.co/Salesforce/blip2-opt-6.7b)
- [instructBlip-7b](https://huggingface.co/Salesforce/instructblip-vicuna-7b)
- [llava1-5-7b](https://huggingface.co/llava-hf/llava-1.5-7b-hf/tree/main)
- [llava1-5-13b](https://huggingface.co/llava-hf/llava-1.5-13b-hf)
- [llava1-6-7b](https://huggingface.co/llava-hf/llava-v1.6-mistral-7b-hf)
- [mantis](https://huggingface.co/TIGER-Lab/Mantis-llava-7b)
- [deepseek](https://huggingface.co/deepseek-ai/deepseek-vl-7b-chat)

### 1.5. output
All generated output is saved in ./output. 

- Logs
Contains all logs from fulltest (SLURM log)
- Model Answers
    Contains all responses from each model, seperated by experiment and datatset
- statistics
    Contains a statistic for each model and mode, seperated by  experiment and datatset


## 2. Installation
1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. create new env (with Python 3.12)
3. activate env (conda activate myenv)
4. install requirements (conda install --file requirements.txt)
5. Download Models
6. Move model_scripts in sub Ressources
7. run batch


## 3. Reproduce Results
The experiments can be run by the following command
<path_to_experiment>/run_<dataset>.sh <basepath_to_experiment> <generate_questions> <generate_answers>

To run all all experiments with SLURM, look at ./utils/batch_fulltest.sh


## 4. streamlit Demo
Demo is created with [streamlit](https://streamlit.io/) and allows to examine results/answers of each model for each question/ data sample. It also contains the answers of the Baseline project [Link](https://github.com/TIBHannover/cross-modal_entity_consistency)
It can be run with the following command: streamlit run app.py