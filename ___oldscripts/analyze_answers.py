import json
from pprint import pprint
import csv 
import copy
import argparse
from array import *
import itertools

statisticObject = {
       "statistic": {
            "persons": {
            },
            "locations": {
            },
            "events": {
            },
            "multi": {
            }
        }
    }

# - - - - - - - - - - - - - - - - - - - - - -


def simplifyAnswer(input):
    return str(input).lower().strip().replace('.', '').replace('=', '')


# - - - - - - - - - - - - - - - - - - - - - -


def analyzeAnswer(args):
    # iterate over all models
    for modelname in args.models:
        modelAnswers = {}

        # save answers of each iteration
        for i in range(args.iterations):
            with open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/{modelname}_{i}.jsonl", 'r') as file:
                for line in file:
                    answerObject = json.loads(line)
                    if answerObject['questionType'] not in modelAnswers:
                        modelAnswers[answerObject['questionType']] = []
                    modelAnswers[answerObject['questionType']].append(answerObject)

        # evaluation for each questionType
        for questionType in modelAnswers:
            # statisticObject for questionType
            model = copy.deepcopy(statisticObject)
            modelAnswers[questionType] = sorted(modelAnswers[questionType], key=lambda x: x['question_id'])
            
            # prepare evaluation file for questionType
            answerFile = open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/answers_TR/TR_{questionType}_{modelname}.csv", 'w', newline ='')
            with answerFile:
                header = ['entity', 'category', 'modelname', 'correct', 'wrong', 'undefinied']
                writer = csv.DictWriter(answerFile, fieldnames = header)
                writer.writeheader()

                for key, values in itertools.groupby(modelAnswers[questionType], lambda x: x["question_id"]):                    
                    for answer in list(values):
                        # add counter to statistic if not exist
                        if answer['category'] not in model['statistic'][answer['entity']]:
                            model['statistic'][answer['entity']][answer['category']] = (0, 0, 0)
                        current_tuple = model['statistic'][answer['entity']][answer['category']]

                        # check if model answer is correct
                        if simplifyAnswer(answer['truth_label']) == simplifyAnswer(answer['TR']):
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1]+1, current_tuple[2])
                        # check if model answer is wrong
                        elif simplifyAnswer(answer['wrong_label']) == simplifyAnswer(answer['TR']):
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2]+1)
                        # check if model answer is undefinied 
                        else:
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2])

                # add statistic to csv
                for item in model['statistic']:
                    for item2 in model['statistic'][item]:
                        correctPercent = round(model['statistic'][item][item2][1] / model['statistic'][item][item2][0], 2)
                        wrongPercent = round(model['statistic'][item][item2][2] / model['statistic'][item][item2][0], 2)
                        undefiniedPercent = round(1 - correctPercent - wrongPercent, 2)
                        
                        writer.writerows([{'entity': item, 'category': item2, 'modelname': modelname, 'correct': correctPercent, 'wrong': wrongPercent, 'undefinied': undefiniedPercent}])


# - - - - - - - - - - - - - - - - - - - - - -


def analyzePropabilityAnswer(args):
    # iterate over all models
    for modelname in args.models:
        modelAnswers = {}

        # save answers of each iteration
        for i in range(args.iterations):
            with open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/{modelname}_{i}.jsonl", 'r') as file:
                for line in file:
                    answerObject = json.loads(line)
                    if answerObject['questionType'] not in modelAnswers:
                        modelAnswers[answerObject['questionType']] = []
                    modelAnswers[answerObject['questionType']].append(answerObject)

        # evaluation for each questionType
        for questionType in modelAnswers:
            # statisticObject for questionType
            model = copy.deepcopy(statisticObject)
            modelAnswers[questionType] = sorted(modelAnswers[questionType], key=lambda x: x['question_id'])
            
            # prepare evaluation file for questionType
            answerFile = open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/answers_PBTR/PBTR_{questionType}_{modelname}.csv", 'w', newline ='')
            with answerFile:
                header = ['entity', 'category', 'modelname', 'correct', 'wrong', 'undefinied']
                writer = csv.DictWriter(answerFile, fieldnames = header)
                writer.writeheader()

                for key, values in itertools.groupby(modelAnswers[questionType], lambda x: x["question_id"]):                    
                    for answer in list(values):
                        # add counter to statistic if not exist
                        if answer['category'] not in model['statistic'][answer['entity']]:
                            model['statistic'][answer['entity']][answer['category']] = (0, 0, 0)
                        current_tuple = model['statistic'][answer['entity']][answer['category']]

                        # check if model answer is correct
                        if simplifyAnswer(answer['truth_label']) == simplifyAnswer(answer['PBTR']):
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1]+1, current_tuple[2])
                        # check if model answer is wrong
                        elif simplifyAnswer(answer['wrong_label']) == simplifyAnswer(answer['PBTR']):
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2]+1)
                        # check if model answer is undefinied 
                        else:
                            model['statistic'][answer['entity']][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2])

                # add statistic to csv
                for item in model['statistic']:
                    for item2 in model['statistic'][item]:
                        correctPercent = round(model['statistic'][item][item2][1] / model['statistic'][item][item2][0], 2)
                        wrongPercent = round(model['statistic'][item][item2][2] / model['statistic'][item][item2][0], 2)
                        undefiniedPercent = round(1 - correctPercent - wrongPercent, 2)
                        
                        writer.writerows([{'entity': item, 'category': item2, 'modelname': modelname, 'correct': correctPercent, 'wrong': wrongPercent, 'undefinied': undefiniedPercent}])


# - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    analyzeAnswer(args)
    analyzePropabilityAnswer(args)



