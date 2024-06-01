import os
import json
import torch
import numpy
import argparse
from PIL import Image
import datetime
import math
import sys
from tqdm import tqdm
import random

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
device = "cuda"
torch.manual_seed(42)

entityObjects = [
    {
        "name": "persons",
        "entities": [],
    },
    {
        "name": "locations",
        "entities": [],
    },
    {
        "name": "events",
        "entities": [],
    }
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()   

def generateQuestions(size):
    tamperednewsData = []
    print("  - load full base dataset")
    with open('./_datasets/tamperednews/_data/tamperednews_train.jsonl', 'r') as f:
        for line in f:
            tamperednewsData.append(json.loads(line))

    print("  - load entities")
    for entityObject in entityObjects:
        with open(f"./_datasets/tamperednews/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

    baseLineobject = {
        "persons": [],
        "locations": [],
        "events": []
    }
    paths = [
        "/nfs/home/ernstd/masterthesis_scripts/output/cnn-baseline/tamperednews_events_scene_similarities.jsonl",
        "/nfs/home/ernstd/masterthesis_scripts/output/cnn-baseline/tamperednews_events_vise_similarities.jsonl",
        "/nfs/home/ernstd/masterthesis_scripts/output/cnn-baseline/tamperednews_locations-indoor_similarities.jsonl",
        "/nfs/home/ernstd/masterthesis_scripts/output/cnn-baseline/tamperednews_locations-outdoor_similarities.jsonl",
        "/nfs/home/ernstd/masterthesis_scripts/output/cnn-baseline/tamperednews_persons_similarities.jsonl"
    ]
    print("  - load baseline similarities")
    for path in paths:
        with open(f"{path}", 'r') as file:
            for line in file:
                lineObject = json.loads(line)
                object = {
                    "document_id": lineObject["document_id"],
                    "similarities": lineObject["similarities"]["untampered"]
                }
                baseLineobject[path.split("_")[2].split("_")[0].split("-")[0]].append(object)

    print("  - sort baseline similarities")
    baseLineobject["persons"].sort(key=lambda x: x["similarities"], reverse=True)
    baseLineobject["locations"].sort(key=lambda x: x["similarities"], reverse=True)
    baseLineobject["events"].sort(key=lambda x: x["similarities"], reverse=True)

    print("  - pick best choices")
    selectionBaselineObjects = baseLineobject["persons"][:int(size/3)] + baseLineobject["locations"][:int(size/3)] + baseLineobject["events"][:int(size/3)]
    
    print("  - get objects from dataset")
    documents = []
    for object in selectionBaselineObjects:
        data = [item for item in tamperednewsData if item.get('id')==object["document_id"]]
        if data:
            documents.append(data[0])      

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    trainQuestions = []
    valQuestions = []
    testQuestions = []

    length = 0
    for lineObject in documents:
        for entityObject in entityObjects:
            for key in lineObject['test_' + entityObject['name']]:
                length += 1

    counter = 0
    for lineObject in documents:
        for entityObject in entityObjects:
            baseQuestion = "\"Decide which <types> set is more consistent to the image: A=<set1> or B=<set2>. Answer only with the name of the set.\""            
            # test entites
            for key in lineObject['test_' + entityObject['name']]:
                question = baseQuestion.replace("<types>", entityObject['name'])
                set_1 = str([extractNameById(id, entityObject['entities']) for id in lineObject['test_' + entityObject['name']]['untampered']])
                set_2 = str([extractNameById(id, entityObject['entities']) for id in lineObject['test_' + entityObject['name']][key]])

                if (len(question) + len(set_1) + len(set_2)) > 800:
                    continue

                gTruth = "-"
                if (random.randint(0,1) == 0):
                    question = question.replace("<set1>", set_1)
                    question = question.replace("<set2>", set_2)
                    gTruth = "A"
                else:
                    question = question.replace("<set2>", set_2)
                    question = question.replace("<set1>", set_1)
                    gTruth = "B"

                if (counter < 0.75 * length):
                    trainQuestions.append({"id": lineObject['id'], "question": str(question), "gTruth": gTruth})
                elif (counter < 0.9 * length):
                    valQuestions.append({"id": lineObject['id'], "question": str(question), "gTruth": gTruth})
                else:
                    testQuestions.append({"id": lineObject['id'], "question": str(question), "gTruth": gTruth})
                counter += 1
    return trainQuestions, valQuestions, testQuestions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    ct = datetime.datetime.now()
    print("current time: ", ct)

    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=400) 
    args = parser.parse_args()

    img_dir = "/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperednews/full_images"
    
    print("create dataset")
    trainQuestions, valQuestions, testQuestions = generateQuestions(args.sample_size)

    # make train annotation
    train_annotation = []
    for question in tqdm(trainQuestions):
        image_url = os.path.join(img_dir, f"{question['id']}.jpg")
        ann = {
            "image": image_url,
            "question": question['question'],
            "gTruth" : question['gTruth'],
            "question_id" : question['id']
        }
        train_annotation.append(ann)

    # make val annotation
    val_annotation = []
    for question in tqdm(valQuestions):
        image_url = os.path.join(img_dir, f"{question['id']}.jpg")
        ann = {
            "image": image_url,
            "question": question['question'],
            "gTruth" : question['gTruth'],
            "question_id" : question['id']
        }
        val_annotation.append(ann)
        
    # make test annotation
    test_annotation = []
    for question in tqdm(testQuestions):
        image_url = os.path.join(img_dir, f"{question['id']}.jpg")
        ann = {
            "image": image_url,
            "question": question['question'],
            "gTruth" : question['gTruth'],
            "question_id" : question['id']
        }
        test_annotation.append(ann)

    with open("./experiments/03_fine_tuning/310_train/_dataset/dataset_train.json", 'w') as file:
        json.dump(train_annotation, file)

    with open("./experiments/03_fine_tuning/310_train/_dataset/dataset_test.json", 'w') as file:
        json.dump(test_annotation, file)

    with open("./experiments/03_fine_tuning/310_train/_dataset/dataset_val.json", 'w') as file:
        json.dump(val_annotation, file)
        
    print("finished datasets")

