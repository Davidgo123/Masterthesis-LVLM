import json
from pprint import pprint


models = [
     {
        "filename": 'instructblip_answers.jsonl',
        "answers": [],
        "statistic": {
            "persons": {
                "verified documents": 0,
                "results": {

                }
            },
            "locations": {
                "verified documents": 0,
                "results": {

                }
            },
            "events": {
                "verified documents": 0,
                "results": {

                }
            },
            "multi": {
                "verified documents": 0,
                "results": {

                }
            }
        }
    },
    {
        "filename": 'llava_1_5_7_answers.jsonl',
        "answers": [],
        "statistic": {
            "persons": {
                "verified documents": 0,
                "results": {

                }
            },
            "locations": {
                "verified documents": 0,
                "results": {

                }
            },
            "events": {
                "verified documents": 0,
                "results": {

                }
            },
            "multi": {
                "verified documents": 0,
                "results": {

                }
            }
        }
    },
    {
        "filename": 'llava_1_5_13_answers.jsonl',
        "answers": [],
        "statistic": {
            "persons": {
                "verified documents": 0,
                "results": {

                }
            },
            "locations": {
                "verified documents": 0,
                "results": {

                }
            },
            "events": {
                "verified documents": 0,
                "results": {

                }
            }, 
            "multi": {
                "verified documents": 0,
                "results": {

                }
            }
        }
    }
]

# - - - - - - - - - - -

def loadModelAnswers(model):
    with open(f"/nfs/home/ernstd/data/news400/document_verification/{model['filename']}", 'r') as file:
        for line in file:
            model['answers'].append(json.loads(line))

# - - - - - - - - - - -


# iterate over all answerfiles
for model in models:
    loadModelAnswers(model)

    for answer in model['answers']:

        # counter for testcases
        if str(answer['test_label']) == "random":
            model['statistic'][answer['test_entity']]['verified documents'] += 1
        if str(answer['test_label']) == "multi":
            model['statistic']['all']['verified documents'] += 1

        # check if truth_label is in response text
        if str(answer['truth_label']).lower() == str(answer['text']).lower().strip():

            # add counter to statistic or increase counter
            if answer['test_label'] not in model['statistic'][answer['test_entity']]['results']:
                model['statistic'][answer['test_entity']]['results'][answer['test_label']] = 1
            else:
                model['statistic'][answer['test_entity']]['results'][answer['test_label']] += 1 

    
    for statistic in model['statistic']:
        for result in model['statistic'][statistic]['results']:
            model['statistic'][statistic]['results'][result] = f"{str(round(float(model['statistic'][statistic]['results'][result])))} ({str(round(float(model['statistic'][statistic]['results'][result]) / (model['statistic'][statistic]['verified documents']) * 100))}%)"

for model in models:
    print(f"--> {model['filename']}")
    pprint(model['statistic'], indent=2, sort_dicts=False, width=70)
    print("\n")






