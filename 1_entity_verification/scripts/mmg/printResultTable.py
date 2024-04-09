import json
import csv
import re
from pprint import pprint
import csv 
import argparse
from array import *


resultsCNN = {
    'locations': {
        'city',
        'country',
        'continent'
    }
}

def getValue(data, entity, testlabel):
    for item in data:
        if item['entity'] == entity and item['testlabel'] == testlabel:
            return item['correct']

def printResults(args):
    resultsVLM = {}
    for modelname in args.models:
        # create object for model
        if modelname not in resultsVLM:
            resultsVLM[modelname] = []

        # read csv content
        with open(f"/nfs/home/ernstd/masterthesis_scripts/1_entity_verification/model_answers/mmg/evaluation/{modelname}.csv", 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                resultsVLM[modelname].append(row)

    for entityType in resultsCNN:
        for testlabel in resultsCNN[entityType]:

            sentence_1 = "%s & %s & %s & %s & %s \\\\" % (
                getValue(resultsVLM['instructBlip_answers'], entityType, testlabel), 
                getValue(resultsVLM['blip_2_answers'], entityType, testlabel), 
                getValue(resultsVLM['llava_1_5_7b_answers'], entityType, testlabel), 
                getValue(resultsVLM['llava_1_5_13b_answers'], entityType, testlabel),
                getValue(resultsVLM['llava_1_6_7b_answers'], entityType, testlabel))


            maxValue = max([float(num) for num in re.findall(r'\d+\.\d+', sentence_1)])
            sentence_1 = sentence_1.replace(str(maxValue), r'\textbf{' + str(maxValue) + r'}')

            print("        " + sentence_1)
        print()
        
# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    printResults(args)