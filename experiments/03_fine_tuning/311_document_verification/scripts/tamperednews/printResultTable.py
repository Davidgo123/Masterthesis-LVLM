import json
import csv
import re
from pprint import pprint
import csv 
import argparse
from array import *


resultsCNN = {
    'persons': {
        'random': '0.95',
        'country-sensitive': '0.92',
        'gender-sensitive': '0.95',
        'country-gender-sensitive': '0.92',
    },
    'locations': {
        'random': '0.85',
        'city-region': '0.74',
        'country-continent': '0.84',
        'region-country': '0.80',
    },
    'events': {
        'random': '1.00',
        'same_instance': '0.74'
    },
}

def getValue(data, entity, category):
    for item in data:
        if item['entity'] == entity and item['category'] == category:
            return item['correct']

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
        for category in resultsCNN[entityType]:

            sentence_0 = ("%s & %s & " % (category, resultsCNN[entityType][category])).replace('_', '-')
            sentence_1 = "%s & %s & %s & %s & %s \\\\" % (
                getValue(resultsVLM[args.models[0]], entityType, category), 
                getValue(resultsVLM[args.models[1]], entityType, category), 
                getValue(resultsVLM[args.models[2]], entityType, category), 
                getValue(resultsVLM[args.models[3]], entityType, category),
                getValue(resultsVLM[args.models[4]], entityType, category))
            maxValue = max([float(num) for num in re.findall(r'\d+\.\d+', sentence_1)])
            sentence_1 = sentence_1.replace(str(maxValue), r'\textbf{' + str(maxValue) + r'}')

            print("        " + sentence_0 + sentence_1)
        print()
        
# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    printResults(args)