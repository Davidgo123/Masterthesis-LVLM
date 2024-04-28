import streamlit as st
import pandas as pd
import json
import os
import glob

st.set_page_config(layout="wide")

# - - - - - - - - - - - - - - - - - - - - - -
#       Variables
# - - - - - - - - - - - - - - - - - - - - - -

answerFiles = []
for files in glob.glob("./output/model_answers/*"):
    answerFiles.append(files.split("\\")[-1])

# - - - - - - - - - - - - - - - - - - - - - -
#       Select Mode & Dataset
# - - - - - - - - - - - - - - - - - - - - - -
col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox('Mode',(sorted(set([i.split("-")[0] for i in answerFiles]))))

with col2:
    dataset = st.selectbox(
        'Dataset',(sorted(set([i.split("-")[1] for i in answerFiles if mode in i])))
    )

# - - - - - - - - - - - - - - - - - - - - - -
#       extract Answers
# - - - - - - - - - - - - - - - - - - - - - -
questions = []
groupedModelAnswers = {}

if mode and dataset:
    models = sorted(set([i.split("-")[2].split(".")[0] for i in answerFiles if mode in i and dataset in i]))
    
    questionPath = ""
    for root, dirs, files in os.walk("./experiments/"):
        questionPath = next((s for s in dirs if mode.split("_")[0] in s), None)
        if questionPath:
            questionPath = os.path.join(root, questionPath)
            break
        
    with open(f"./{questionPath}/_questions/questions_{dataset}.jsonl", mode='r', encoding="utf-8") as file:
        for line in file:
            questions.append(json.loads(line))

    # iterate over all models
    for modelname in models:
        # get all model answers and group them by entity type (location)
        with open(f"./output/model_answers/{mode}-{dataset}-{modelname}.jsonl", mode='r', encoding="utf-8") as file:
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
selectedQuestionID = st.selectbox(
    'questionID',
    (list(set(item["question_id"] for item in questions))),
    key="selectedQuestionID"
)

# - - - - - - - - - - - - - - - - - - - - - -
#       Show Image
# - - - - - - - - - - - - - - - - - - - - - -
if os.path.exists(f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.png"):
    st.image(f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.png", width=800)
elif os.path.exists(f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.jpg"):
    st.image(f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.jpg", width=800)
else:
    st.write("Image not found.")


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
if mode == "11_DV":
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
