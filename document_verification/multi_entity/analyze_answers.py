import json
from pprint import pprint
import csv 
import copy
import argparse

modelnames = ['instructBlip', 'blip_2', 'llava_1_5_7', 'llava_1_5_13']

statisticObject = {
       "filename": "",
       "statistic": {
                        "persons": {
                            "verified_documents": 0,
                            "results": {

                            }
                        },
                        "locations": {
                            "verified_documents": 0,
                            "results": {

                            }
                        },
                        "events": {
                            "verified_documents": 0,
                            "results": {

                            }
                        },
                        "multi": {
                            "verified_documents": 0,
                            "results": {

                            }
                        }
                    }
                }

# - - - - - - - - - - -

def simplifyAnswer(input):
    return str(input).lower().strip().replace('.', '').replace('=', '')

# - - - - - - - - - - -

def run_analyze(args):
    answerFile = open('/nfs/home/ernstd/data/news400/document_verification/multi_entity/answers.csv', 'w', newline ='')
    with answerFile:
        header = ['entity', 'category', 'modelname', 'correct', 'wrong', 'undefinied']
        writer = csv.DictWriter(answerFile, fieldnames = header)
        writer.writeheader()

        # iterate over all models
        for modelname in modelnames:
            
            modelAnswers = []

            # load answers of each iteration
            for i in range(args.iterations):
                model = copy.deepcopy(statisticObject)
                model['filename'] = f"{modelname}_answers_{i}.jsonl"
                
                # load answers
                with open(f"/nfs/home/ernstd/data/news400/document_verification/multi_entity/{model['filename']}", 'r') as file:
                    for line in file:
                        modelAnswers.append(json.loads(line))

            # run over all answers
            for answer in modelAnswers:

                # add counter to statistic if not exist
                if answer['category'] not in model['statistic'][answer['entity']]['results']:
                    model['statistic'][answer['entity']]['results'][answer['category']] = (0, 0, 0)

                current_tuple = model['statistic'][answer['entity']]['results'][answer['category']]

                # check if model answer is correct
                if simplifyAnswer(answer['truth_label']) == simplifyAnswer(answer['text']):
                    model['statistic'][answer['entity']]['results'][answer['category']] = (current_tuple[0]+1, current_tuple[1]+1, current_tuple[2])

                # check if model answer is wrong
                elif simplifyAnswer(answer['wrong_label']) == simplifyAnswer(answer['text']):
                    model['statistic'][answer['entity']]['results'][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2]+1)
                
                else:
                    model['statistic'][answer['entity']]['results'][answer['category']] = (current_tuple[0]+1, current_tuple[1], current_tuple[2])

            # add statistic to csv
            for item in model['statistic']:
                for item2 in model['statistic'][item]['results']:
                    correctPercent = round(model['statistic'][answer['entity']]['results'][answer['category']][1] / model['statistic'][answer['entity']]['results'][answer['category']][0], 2)
                    wrongPercent = round(model['statistic'][answer['entity']]['results'][answer['category']][2] / model['statistic'][answer['entity']]['results'][answer['category']][0], 2)
                    undefiniedPercent = round(1 - correctPercent - wrongPercent, 2)
                    
                    writer.writerows([{'entity': item, 'category': item2, 'modelname': modelname, 'correct': correctPercent, 'wrong': wrongPercent, 'undefinied': undefiniedPercent}])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1)
    args = parser.parse_args()
    run_analyze(args)



