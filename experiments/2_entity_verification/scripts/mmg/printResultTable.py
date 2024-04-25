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

def getDocuments(data, entity, testlabel):
    for item in data:
        if item['entity'] == entity and item['testlabel'] == testlabel:
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
        for testlabel in resultsCNN[entityType]:

            sentence_1 = "%s & %s & %s & %s & %s \\\\" % (
                getValue(resultsVLM[args.models[0]], entityType, testlabel), 
                getValue(resultsVLM[args.models[1]], entityType, testlabel), 
                getValue(resultsVLM[args.models[2]], entityType, testlabel), 
                getValue(resultsVLM[args.models[3]], entityType, testlabel),
                getValue(resultsVLM[args.models[4]], entityType, testlabel))


            maxValue = max([float(num) for num in re.findall(r'\d+\.\d+', sentence_1)])
            sentence_1 = sentence_1.replace(str(maxValue), r'\textbf{' + str(maxValue) + r'}')

            print(f"        {testlabel} & {getDocuments(resultsVLM['instructBlip_answers'], entityType, testlabel)} & {sentence_1}")
        print()
        
# - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs='*')
    args = parser.parse_args()
    printResults(args)