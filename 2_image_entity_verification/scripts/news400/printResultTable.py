import json
import csv
import re
from pprint import pprint
import csv 
import argparse
from array import *


resultsCNN = {
    "persons": {
        "orginal"
    },
    "locations": {
        "orginal"
    },
    "events": {
        "orginal"
    }
}

def getValue(data, entity):
    for item in data:
        if item['entity'] == entity:
            return item['correct']

def printResults(args):
    resultsVLM = {}
    for modelname in args.models:
        # create object for model
        if modelname not in resultsVLM:
            resultsVLM[modelname] = []

        # read csv content
        with open(f"/nfs/home/ernstd/masterthesis_scripts/2_image_entity_verification/model_answers/news400/evaluation/{modelname}.csv", 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                resultsVLM[modelname].append(row)

    for entityType in resultsCNN:
        sentence_1 = "%s & %s & %s & %s & %s \\\\" % (
            getValue(resultsVLM['instructBlip_answers'], entityType), 
            getValue(resultsVLM['blip_2_answers'], entityType), 
            getValue(resultsVLM['llava_1_5_7b_answers'], entityType), 
            getValue(resultsVLM['llava_1_5_13b_answers'], entityType),
            getValue(resultsVLM['llava_1_6_7b_answers'], entityType))

        maxValue = max([float(num) for num in re.findall(r'\d+\.\d+', sentence_1)])
        sentence_1 = sentence_1.replace(str(maxValue), r'\textbf{' + str(maxValue) + r'}')

        print("        " + sentence_1)

        
# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    printResults(args)