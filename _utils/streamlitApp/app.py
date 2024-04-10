import streamlit as st
import pandas as pd
import json

# - - - - - - - - - - - - - - - - - - - - - -
#       Select Mode & Dataset
# - - - - - - - - - - - - - - - - - - - - - -

mode = st.selectbox(
    'Mode',
    (
        '0_document_verification', 
        '1_entity_verification', 
        '2_image_entity_verification',
        '3_max_image_entity_verification'
     )
)

dataset = st.selectbox(
    'Dataset',
    (
        'news400', 
        'tamperedNews', 
        'mmg'
     )
)



# - - - - - - - - - - - - - - - - - - - - - -
#       extract Answers
# - - - - - - - - - - - - - - - - - - - - - -

models = ['blip_2', 'instructBlip', 'llava_1_5_7b', 'llava_1_5_13b', 'llava_1_6_7b']
groupedModelAnswers = {}
questionIDs = []

if mode and dataset:
    with open(f"../../{mode}/_questions/questions_{dataset}.jsonl", mode='r') as file:
        for line in file:
            questionObject = json.loads(line)
            questionIDs.append(questionObject['question_id'])

    # iterate over all models
    for modelname in models:
        # get all model answers and group them by entity type (location)
        with open(f"../../{mode}/model_answers/{dataset}/{modelname}.jsonl", mode='r') as file:
            for line in file:
                answerObject = json.loads(line)
                entityType = answerObject['entity']
                testlabel = answerObject['testlabel']
                questionID = answerObject['question_id']

                if modelname not in groupedModelAnswers:
                    groupedModelAnswers[modelname] = {}

                # filter by entity type
                if entityType not in groupedModelAnswers[modelname]:
                    groupedModelAnswers[modelname][entityType] = {}
                
                # filter by testlabel
                if testlabel not in groupedModelAnswers[modelname][entityType]:
                    groupedModelAnswers[modelname][entityType][testlabel] = {}
                
                # filter by question id
                if questionID not in groupedModelAnswers[modelname][entityType][testlabel]:
                    groupedModelAnswers[modelname][entityType][testlabel][questionID] = []

                # append question
                groupedModelAnswers[modelname][entityType][testlabel][questionID].append(answerObject)



# - - - - - - - - - - - - - - - - - - - - - -
#       Select Question
# - - - - - - - - - - - - - - - - - - - - - -

dataset = st.selectbox(
    'Dataset',
    (questionIDs)
)



# - - - - - - - - - - - - - - - - - - - - - -
#       Show Image
# - - - - - - - - - - - - - - - - - - - - - -

#st.button("Reset", type="primary")
#if st.button('Say hello'):
#    st.write('Why hello there')
#else:
#    st.write('Goodbye')

#st.image('sunrise.jpg', caption='Sunrise by the mountains')