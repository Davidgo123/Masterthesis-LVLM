import streamlit as st
import pandas as pd
import json
import os
import glob

st.set_page_config(layout="wide")

# - - - - - - - - - - - - - - - - - - - - - -
#       Variables
# - - - - - - - - - - - - - - - - - - - - - -
for files in glob.glob("./outputs/"):
    print(files)
    
# - - - - - - - - - - - - - - - - - - - - - -
#       Select Mode & Dataset
# - - - - - - - - - - - - - - - - - - - - - -
col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox(
        'Mode',
        (
            'experiments/01_without_comparative_images/11_document_verification', 
            'experiments/01_without_comparative_images/12_entity_verification'
            'experiments/02_with_comparative_images/21_single_input_models/entity_verification_1x1', 
            'experiments/02_with_comparative_images/21_single_input_models/entity_verification_1xN', 
            'experiments/02_with_comparative_images/22_multi_input_models/entity_verification_1x1', 
            'experiments/02_with_comparative_images/22_multi_input_models/entity_verification_1xN', 
        )
    )
with col2:
    datasets = ["news400", "tamperednews", "mmg"]
    models = ['blip2', 'instructBlip', 'llava_15_7b', 'llava_15_13b', 'llava_16_7b']
    if mode == "experiments/02_with_comparative_images/21_single_input_models/entity_verification_1x1":
        datasets = ["news400", "tamperednews"]
    if mode == "experiments/02_with_comparative_images/21_single_input_models/entity_verification_1xN":
        datasets = ["tamperedNews"]
    if  mode == "experiments/02_with_comparative_images/22_multi_input_models/entity_verification_1x1":
        models = ['mantis', 'deepseek']
        datasets = ["news400", "tamperednews"]
    if mode == "experiments/02_with_comparative_images/22_multi_input_models/entity_verification_1xN":
        datasets = ["tamperedNews"]
        models = ['mantis', 'deepseek']

    dataset = st.selectbox(
        'Dataset',(datasets)
    )

# - - - - - - - - - - - - - - - - - - - - - -
#       extract Answers
# - - - - - - - - - - - - - - - - - - - - - -
groupedModelAnswers = {}
questionIDs = []
imageIDs = []

if mode and dataset:
    with open(f"./{mode}/_questions/questions_{dataset}.jsonl", mode='r', encoding="utf-8") as file:
        for line in file:
            questionObject = json.loads(line)
            questionIDs.append(questionObject['question_id'])
            imageIDs.append(questionObject['image'].split("/")[-1])

    # iterate over all models
    for modelname in models:
        # get all model answers and group them by entity type (location)
        with open(f"./{mode}/model_answers/{dataset}/{modelname}_answers.jsonl", mode='r', encoding="utf-8") as file:
            for line in file:
                answerObject = json.loads(line)
                entityType = answerObject['entity']
                testlabel = answerObject['testlabel']
                questionID = answerObject['question_id']

                # filter by id
                if questionID not in groupedModelAnswers:
                    groupedModelAnswers[questionID] = {}
                
                # filter by entity type 
                if entityType not in groupedModelAnswers[questionID]:
                    groupedModelAnswers[questionID][entityType] = {}
                
                # filter by testlabel
                if testlabel not in groupedModelAnswers[questionID][entityType]:
                    groupedModelAnswers[questionID][entityType][testlabel] = {}

                # filter by model
                if modelname not in groupedModelAnswers[questionID][entityType][testlabel]:
                    groupedModelAnswers[questionID][entityType][testlabel][modelname] = []
                
                groupedModelAnswers[questionID][entityType][testlabel][modelname].append(answerObject)

# - - - - - - - - - - - - - - - - - - - - - -
#       Select Question
# - - - - - - - - - - - - - - - - - - - - - -
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

def click_button1(list):
    st.session_state['current_index'] = (st.session_state['current_index'] + 1) % len(list)
    st.session_state.selectedQuestionID = list[st.session_state['current_index']]

def click_button2(list):
    st.session_state['current_index'] = (st.session_state['current_index'] - 1) % len(list)
    st.session_state.selectedQuestionID = list[st.session_state['current_index']]

def update_list(list):
    st.session_state['current_index'] = list.index(st.session_state.selectedQuestionID)


selectedQuestionID = st.selectbox(
    'questionID',
    (list(set(questionIDs))),
    key="selectedQuestionID",
    on_change=update_list,
    args=[list(set(questionIDs))]
)

# - - - - - - - - - - - - - - - - - - - - - -
#       Show Image
# - - - - - - - - - - - - - - - - - - - - - -
png_path = f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.png"
jpg_path = f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.jpg"

if mode == "experiments/3_image_entity_verification":
    selectedEntityID = st.selectbox(
        'entityID',
        list(filter(lambda x: selectedQuestionID in x, imageIDs)),
        key="selectedEntityID",
    )
    png_path = f"./experiments/3_image_entity_verification/images/{dataset}/{selectedEntityID}"
    jpg_path = f"./experiments/3_image_entity_verification/images/{dataset}/{selectedEntityID}"

col1, col2 = st.columns([8, 1])
with col1:
    if os.path.exists(png_path):
        st.image(png_path, width=800)
    elif os.path.exists(jpg_path):
        st.image(jpg_path, width=800)
    else:
        st.write("Image not found.")
with col2:
    st.button("Next", type="primary", on_click=click_button1, args=[list(set(questionIDs))])
    st.button("Previous", type="primary", on_click=click_button2, args=[list(set(questionIDs))])


# - - - - - - - - - - - - - - - - - - - - - -
#       select entityType & testLabel
# - - - - - - - - - - - - - - - - - - - - - -
col1, col2 = st.columns(2)
with col1:
    selectedEntityType = st.selectbox('entityType',
        (list(groupedModelAnswers[st.session_state.selectedQuestionID]))
    )
with col2:
    selectedTestLabel = st.selectbox('testLabel',
        (list(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType]))
    )

# - - - - - - - - - - - - - - - - - - - - - -
#       Grid
# - - - - - - - - - - - - - - - - - - - - - -
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


# - - - - - - - - - - - - - - - - - - - - - -
#       Max Scores
# - - - - - - - - - - - - - - - - - - - - - -

# find max prob val in all sets (text and test)
maxScoreAnswer = {}
for model in models:
    # Filter objects with "yes" in the "response" key
    filtered_objects = list(filter(lambda x: x["response"].lower().strip() == "yes", groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model][:]))
    if filtered_objects:
        # If there are objects with "yes" response, get the object with maximum value
        maxScoreAnswer[model] = max(filtered_objects, key=lambda x: x["prob"])
    else:
        # If there are no objects with "yes" response, get the object with minimum value
        maxScoreAnswer[model] = min(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model][:], key=lambda x: x["prob"])


# - - - - - - - - - - - - - - - - - - - - - -
#       Content Table
# - - - - - - - - - - - - - - - - - - - - - -
sets = ["text"]
if mode == "experiments/1_document_verification":
    sets.append("test")

if mode == "2_image_entity_verification":
    for model in models:
        groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model] = list(filter(lambda x: selectedEntityID in x["image"], groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model]))

for set in sets:
    cols = len([x for x in groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][models[0]][:] if x['set'] == set]), # questions
    rows = len(list(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel])) + 1 # question + all models
    
    grid_text = make_grid(cols[0] + 1, rows)
    st.write("#")
    st.write("#")

    for colCounter in range(cols[0] + 1):
        for rowCounter in range(rows):
            answer = list([x for x in sorted(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][models[rowCounter-1]][:], key = lambda x: (x['set'], x['question'])) if x['set'] == set])[colCounter - 1].copy()
            
            # print header
            if colCounter == 0:
                if rowCounter == 0:
                    grid_text[colCounter][rowCounter].write(f"Questions ({set})")
                elif set == 'text':
                    grid_text[colCounter][rowCounter].write(f":blue[{models[rowCounter-1]}]")
                elif set == 'test':
                    grid_text[colCounter][rowCounter].write(f":red[{models[rowCounter-1]}]")
            
            # print question
            elif rowCounter == 0 and colCounter != 0:
                grid_text[colCounter][rowCounter].write(f"{answer['question']} ({answer['gTruth']})")
                
            # print answers
            else:
                if mode == "0_document_verification":
                    if answer == maxScoreAnswer[models[rowCounter-1]]:
                        if set == "text":
                            grid_text[colCounter][rowCounter].write(f":blue[{answer['response']} ({answer['prob']})]")
                        elif set == "test":
                            grid_text[colCounter][rowCounter].write(f":red[{answer['response']} ({answer['prob']})]")
                    else:
                        grid_text[colCounter][rowCounter].write(f"{answer['response']} ({answer['prob']})")

                else:
                    if str(answer["gTruth"]) == str(answer["response"]).lower().strip():
                        grid_text[colCounter][rowCounter].write(f":blue[{answer['response']} ({answer['prob']})]")
                    else:
                        grid_text[colCounter][rowCounter].write(f":red[{answer['response']} ({answer['prob']})]")
