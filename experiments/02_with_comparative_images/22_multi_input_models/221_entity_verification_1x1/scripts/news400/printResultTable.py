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
        
def getDocuments(data, entity):
    for item in data:
        if item['entity'] == entity:
            return item['documents']

def printResults(args):
    resultsVLM = {}
    for modelname in args.models:
        # create object for model
        if modelname not in resultsVLM:
            resultsVLM[modelname] = []

        # read csv content
        with open(f"./output/statistics/{modelname}.csv", 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                resultsVLM[modelname].append(row)

    for entityType in resultsCNN:
        sentence_1 = "%s & %s & %s & %s & %s \\\\" % (
            getValue(resultsVLM[args.models[0]], entityType), 
            getValue(resultsVLM[args.models[1]], entityType), 
            getValue(resultsVLM[args.models[2]], entityType), 
            getValue(resultsVLM[args.models[3]], entityType),
            getValue(resultsVLM[args.models[4]], entityType))

        maxValue = max([float(num) for num in re.findall(r'\d+\.\d+', sentence_1)])
        sentence_1 = sentence_1.replace(str(maxValue), r'\textbf{' + str(maxValue) + r'}')

        print(f"        {entityType} & {getDocuments(resultsVLM[args.models[0]], entityType)} & {sentence_1}")

        
# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    printResults(args)