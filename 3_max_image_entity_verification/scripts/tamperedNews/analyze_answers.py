import json
from pprint import pprint
import csv 
import copy
import argparse
from array import *

statisticObject = {
       "statistic": {
            "persons": {
            },
            "locations": {
            },
            "events": {
            }
        }
    }

# - - - - - - - - - - - - - - - - - - - - - -

def simplifyAnswer(answer):
    return str(answer).lower().strip().replace('.', '').replace('=', '')

def computeAnswer(args):
    # iterate over all models
    for modelname in args.models:
        groupedModelAnswers = {}

        # get all model answers and group them by entity type (person, location, event)
        with open(f"/nfs/home/ernstd/masterthesis_scripts/3_max_image_entity_verification/model_answers/tamperedNews/{modelname}.jsonl", 'r') as file:
            for line in file:
                answerObject = json.loads(line)
                entityType = answerObject['entity']
                testlabel = answerObject['testlabel']
                questionID = answerObject['question_id']

                # filter by entity type
                if entityType not in groupedModelAnswers:
                    groupedModelAnswers[entityType] = {}
                
                # filter by testlabel
                if testlabel not in groupedModelAnswers[entityType]:
                    groupedModelAnswers[entityType][testlabel] = {}
                
                # filter by question id
                if questionID not in groupedModelAnswers[entityType][testlabel]:
                    groupedModelAnswers[entityType][testlabel][questionID] = []

                # append question
                groupedModelAnswers[entityType][testlabel][questionID].append(answerObject)

        # statisticObject
        model = copy.deepcopy(statisticObject)

        # evaluation for each entity type (person, location, event)
        for entityType in groupedModelAnswers:
            for testlabel in groupedModelAnswers[entityType]:
                for questionID in groupedModelAnswers[entityType][testlabel]:

                    # iterate over each question of same id and compute score
                    maxValues = {
                        "yes": 0.0,
                        "no": 0.0
                    }
                    for question in groupedModelAnswers[entityType][testlabel][questionID]:
                        if simplifyAnswer(question['response']) == 'yes' and simplifyAnswer(question['probText']) == 'yes':
                            if maxValues['yes'] < float(question['prob']):
                                maxValues['yes'] = float(question['prob'])
                        elif simplifyAnswer(question['response']) == 'no' and simplifyAnswer(question['probText']) == 'no':
                            if maxValues['no'] < float(question['prob']):
                                maxValues['no'] = float(question['prob'])

                    # add counter to statistic if not exist
                    if testlabel not in model['statistic'][entityType]:
                        model['statistic'][entityType][testlabel] = (0, 0, 0)
                    current_tuple = model['statistic'][entityType][testlabel]

                    # check if model answer is undefinied  
                    if max(maxValues.values()) == 0.0:
                        model['statistic'][entityType][testlabel] = (current_tuple[0]+1, current_tuple[1], current_tuple[2])
                    # check if model answer is correct
                    elif max(maxValues, key=maxValues.get) == question['gTruth']:
                        model['statistic'][entityType][testlabel] = (current_tuple[0]+1, current_tuple[1]+1, current_tuple[2])
                    # check if model answer is wrong
                    elif max(maxValues, key=maxValues.get) == question['gWrong']: 
                        model['statistic'][entityType][testlabel] = (current_tuple[0]+1, current_tuple[1], current_tuple[2]+1)
                
        # prepare evaluation file for questionType
        answerFile = open(f"/nfs/home/ernstd/masterthesis_scripts/3_max_image_entity_verification/model_answers/tamperedNews/evaluation/{modelname}.csv", 'w', newline ='')
        with answerFile:
            header = ['entity', 'testlabel', 'modelname', 'correct', 'wrong', 'undefinied', 'documents']
            writer = csv.DictWriter(answerFile, fieldnames = header)
            writer.writeheader()

            # add statistic to csv
            for item in model['statistic']:
                for item2 in model['statistic'][item]:
                    correctPercent = round(model['statistic'][item][item2][1] / model['statistic'][item][item2][0], 2)
                    wrongPercent = round(model['statistic'][item][item2][2] / model['statistic'][item][item2][0], 2)
                    undefiniedPercent = round(1 - correctPercent - wrongPercent, 2)
                    writer.writerows([{'entity': item, 'testlabel': item2, 'modelname': modelname, 'correct': correctPercent, 'wrong': wrongPercent, 'undefinied': undefiniedPercent, 'documents': model['statistic'][item][item2][0]}])

# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    computeAnswer(args)



