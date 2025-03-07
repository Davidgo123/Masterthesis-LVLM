## 1. Overview
The following project was created for the Master Thesis "Cross-Modal Entity Consistency in News
using Large Vision-Language Models" on Faculty of Electrical Engineering and Computer Science at Institute of Data Science - Leibniz University Hannover. The repository includes multiple scripts, datasets and results to calculate and verify the thesis content.


## 2. Abstract Thesis
Nowadays, the internet has become a central source of information for many people. Since anyone can freely distribute content, the biggest challenge is to distinguish reliable information from misinformation. News often uses different modalities such as image and text to convey content more effectively. However, these modalities can be manipulated by criminals. Due to the amount of information, manual verification is impractical. This thesis presents an approach that analyzes the cross-modal consistency of entities such as people, places, and events in multimodal news articles that contain both text and images. These modalities can be processed by Vision Language Models (VLMs), which have not been used for such tasks before.

A major contribution of this research was to create a high-quality dataset, called Tampered-News-EV, to ensure a reliable basis for the evaluation of documents or entities. Based on this dataset, a novel approach for document verification is presented, which reduces the computational effort and thus optimizes efficiency and performance in real-world applications. In addition, modern VLMs are used to validate individual entities in images and texts. These approaches are accompanied by different prompts for the image-language models to investigate the influence of these formats on different entities. Furthermore, additional information such as evidence images are tested to improve the visual capabilities of the models. Task-specific training methods are applied to refine the models’ understanding of news analysis tasks. The experimental results show that the image-language models are able to achieve high accuracy in document verification and partially verify the consistency of individual entities between the modalities text and image. 

A demonstration application was developed to analyze the results more comprehensively. In the future, further languages and cultural contexts could be taken into account to cover more aspects of messages. The high processing speed and accuracy achieved indicate the potential for real-world applications, such as browser plugins that can validate news content in real time and thus contribute to ongoing efforts to combat misinformation.



## 3. Project Structure

### 3.1. datasets
This Projects includes data from the datatset news400 [link](https://data.uni-hannover.de/dataset/tamperednews-news400-ijmir21), tamperedNews [link](https://data.uni-hannover.de/dataset/tamperednews-news400-ijmir21) and mmg [link](https://link.springer.com/chapter/10.1007/978-3-031-28238-6_14).
Each Dataset contains all used images, the used samples (news400_merged.jsonl, tamperednews.json and test_dataset.json) and the entity mapping data.

### 3.2. experiments
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

### 3.3. model_scripts
Each model requiered different options to generate answers and probailities.
Mantis and Deepseek requiered additional ressources:
- [mantis](https://github.com/TIGER-AI-Lab/Mantis)
- [deepseek](https://github.com/deepseek-ai/DeepSeek-VL)
After download, the scripts (mantis.py and deepseek.py) need to be moved in the downloaded ressource

### 3.4. used vision language models
- [blip-2-7b](https://huggingface.co/Salesforce/blip2-opt-6.7b)
- [instructBlip-7b](https://huggingface.co/Salesforce/instructblip-vicuna-7b)
- [llava1-5-7b](https://huggingface.co/llava-hf/llava-1.5-7b-hf/tree/main)
- [llava1-5-13b](https://huggingface.co/llava-hf/llava-1.5-13b-hf)
- [llava1-6-7b](https://huggingface.co/llava-hf/llava-v1.6-mistral-7b-hf)
- [mantis](https://huggingface.co/TIGER-Lab/Mantis-llava-7b)
- [deepseek](https://huggingface.co/deepseek-ai/deepseek-vl-7b-chat)

### 3.5. output
All generated output is saved in ./output. 

- Logs
Contains all logs from fulltest (SLURM log)
- Model Answers
    Contains all responses from each model, seperated by experiment and datatset
- statistics
    Contains a statistic for each model and mode, seperated by  experiment and datatset


## 4. Installation
1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. create new env (with Python 3.12)
3. activate env (conda activate myenv)
4. install requirements (conda install --file requirements.txt)
5. Download Models
6. Move model_scripts in sub Ressources
7. run batch


## 5. Reproduce Results
The experiments can be run by the following command
<path_to_experiment>/run_<dataset>.sh <basepath_to_experiment> <generate_questions> <generate_answers>

To run all all experiments with SLURM, look at ./utils/batch_fulltest.sh


## 6. streamlit Demo
Demo is created with [streamlit](https://streamlit.io/) and allows to examine results/answers of each model for each question/ data sample. It also contains the answers of the Baseline project [Link](https://github.com/TIBHannover/cross-modal_entity_consistency)
It can be run with the following command: 
- streamlit run app.py
- python -m streamlit run ./streamlitDemo/app.py
- ssh -N -f -L localhost:8501:localhost:8501 devbox5