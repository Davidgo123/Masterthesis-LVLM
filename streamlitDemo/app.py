import streamlit as st
import pandas as pd
import json
import os
import glob
from PIL import Image

st.set_page_config(layout="wide")

def updateTextHeader(text, color):
    if color:
        return f"""<p style="color:{color}; font-size: 18px; font-weight:600;">{text}</p>"""
    return f"""<p style="font-size: 18px; font-weight: 600;">{text}</p>"""

def updateText(text, color):
    if color:
        return f"""<p style="color:{color}; font-size: 18px; font-weight:500;">{text}</p>"""
    return f"""<p style="font-size: 18px; font-weight: 500;">{text}</p>"""

css = '''
<style>
.stSelectbox * {
    font-size: 16px;
    font-weight:500
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

maincol1, maincol2 = st.columns(2)
with maincol1:
    # - - - - - - - - - - - - - - - - - - - - - -
    #       Variables

    questions = []
    baseline = {}
    groupedModelAnswers = {}

    # - - - - - - - - - - - - - - - - - - - - - -

    answerFiles = []
    for files in glob.glob("./output/model_answers/*"):
        if "311" in files.split("\\")[-1] or "312" in files.split("\\")[-1]: # ignore train data
            continue
        if "1x1" in files.split("\\")[-1]: # ignore single evidence image data
            continue
        answerFiles.append(files.split("\\")[-1])

    # - - - - - - - - - - - - - - - - - - - - - -
    #       Select Mode & Dataset
    # - - - - - - - - - - - - - - - - - - - - - -
    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox('Mode',(sorted(set([i.split("/")[-1].split("-")[0] for i in answerFiles]))))

    with col2:
        dataset = st.selectbox(
            'Dataset',(sorted(set([i.split("-")[1] for i in answerFiles if mode in i])))
        )

    # - - - - - - - - - - - - - - - - - - - - - -
    #       extract Answers
    # - - - - - - - - - - - - - - - - - - - - - -
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

        if (mode == "11_DV" or mode == "12_EV") and (dataset == "news400" or dataset == "tamperednews"):
            if "baseline" not in models:
                models.append("baseline")
        print(models)
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
        (sorted(list(set(item["question_id"] for item in questions)))),
        key="selectedQuestionID"
    )

# - - - - - - - - - - - - - - - - - - - - - -
#       Images
# - - - - - - - - - - - - - - - - - - - - - -
with maincol2:
    def resize_image(image_path, new_height):
        with Image.open(image_path) as img:
            width_percent = (new_height / float(img.size[1]))
            new_width = int((float(img.size[0]) * float(width_percent)))
            resized_img = img.resize((new_width, new_height))
            return resized_img

    if mode == "11_DV" or mode == "12_EV":
        st.image(resize_image(glob.glob(f"./_datasets/{dataset}/images/{st.session_state.selectedQuestionID}.*")[0], 300), caption=f"News image ({st.session_state.selectedQuestionID})")


    elif "212_EV_1xN" in mode:
        def format_json_option(json_obj):
            return json_obj['image'].split("/")[-1] 
        with maincol1:
            selectedEntityID = st.selectbox(
                'entityID',
                list(filter(lambda x: selectedQuestionID in x['image'].split("/")[-1], questions)),
                format_func=format_json_option
            )
        st.image(resize_image(selectedEntityID["image"], 400), caption=f"News image (Top), Entity image (Bot)")


    elif "222_EV_1xN" in mode:
        def format_json_option(json_obj):
            return json_obj['entity_image'].split("/")[-2]  + "/" + json_obj['entity_image'].split("/")[-1] 
        with maincol1:
            selectedEntityID = st.selectbox(
                'entityID',
                list(filter(lambda x: selectedQuestionID.split("_")[0] in x["news_image"] and selectedQuestionID.split("_")[1] in x["entity_image"], questions)),
                format_func=format_json_option
            )

        col1, col2 = st.columns(2)
        with col1:
            st.image(resize_image(selectedEntityID["news_image"], 300), caption=f"News image")
        with col2:
            st.image(resize_image(selectedEntityID["entity_image"], 300), caption=f"Entity image") 


    # - - - - - - - - - - - - - - - - - - - - - -
    #       select entityType & testLabel
    # - - - - - - - - - - - - - - - - - - - - - -
with maincol1:
    selectedEntityType = st.selectbox('entityType',
        (list(groupedModelAnswers[st.session_state.selectedQuestionID]))
    )
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
maxScoreAnswer = {}
if mode == "11_DV":
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

elif "211" in mode or "212" in mode:
    for model in models:
        groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model] = list(filter(lambda x: selectedEntityID["image"] in x["image"], groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model]))

elif "221" in mode or "222" in mode:
    for model in models:
        groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model] = list(filter(lambda x: selectedEntityID["entity_image"] in x["entity_image"], groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][model]))

st.markdown("""---""") 
for set in sets:
    cols = len([x for x in groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][models[0]][:] if x['set'] == set]), # questions
    rows = len(list(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel])) + 1 # question + all models
    
    grid_text = make_grid(cols[0] + 1, rows)
    st.markdown("""---""") 
    for colCounter in range(cols[0] + 1):
        for rowCounter in range(rows):
            try:
                answer = list([x for x in sorted(groupedModelAnswers[st.session_state.selectedQuestionID][selectedEntityType][selectedTestLabel][models[rowCounter-1]][:], key = lambda x: (x['set'], x['question'])) if x['set'] == set])[colCounter - 1].copy()
                
                # print header
                if colCounter == 0:
                    if rowCounter == 0:
                        grid_text[colCounter][rowCounter].write(updateTextHeader(f"Questions ({set})", None), unsafe_allow_html=True)
                    elif set == 'text':
                        grid_text[colCounter][rowCounter].write(updateTextHeader(f"{models[rowCounter-1]}", None), unsafe_allow_html=True)
                    elif set == 'test':
                        grid_text[colCounter][rowCounter].write(updateTextHeader(f"{models[rowCounter-1]}", None), unsafe_allow_html=True)
                
                # print question
                elif rowCounter == 0 and colCounter != 0:
                    grid_text[colCounter][rowCounter].write(updateText(f"{answer['question']} ({answer['gTruth']})", None), unsafe_allow_html=True)
                    
                # print answers
                else:
                    if mode == "11_DV":
                        if answer == maxScoreAnswer[models[rowCounter-1]]:
                            if set == "text":
                                grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']} ({answer['prob']})", "blue"), unsafe_allow_html=True)
                            elif set == "test":
                                grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']} ({answer['prob']})", "red"), unsafe_allow_html=True)
                        else:
                            grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']} ({answer['prob']})", None), unsafe_allow_html=True)

                    elif mode == "222_EV_1xN":
                        if str(answer["gTruth"]) == str(answer["response"]).lower().strip():
                            grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']}", "blue"), unsafe_allow_html=True)
                        else:
                            grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']}", "red"), unsafe_allow_html=True)

                    else:
                        if str(answer["gTruth"]) == str(answer["response"]).lower().strip():
                            grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']} ({answer['prob']})", "blue"), unsafe_allow_html=True)
                        else:
                            grid_text[colCounter][rowCounter].write(updateText(f"{answer['response']} ({answer['prob']})", "red"), unsafe_allow_html=True)
            except:
                grid_text[colCounter][rowCounter].write(updateText(f" - ", "red"), unsafe_allow_html=True)