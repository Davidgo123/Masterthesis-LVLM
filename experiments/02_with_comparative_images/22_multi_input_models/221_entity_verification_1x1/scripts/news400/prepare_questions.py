import json
import argparse
from PIL import Image
import numpy as np
import glob

entityObjects = [
    {
        "name": "persons",
        "label": "annotation_persons",
        "entities": [],
    },
    {
        "name": "locations",
        "label": "annotation_locations",
        "entities": [],
    },
    {
        "name": "events",
        "label": "annotation_events",
        "entities": [],
    }
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def loadEntities():
    for entityObject in entityObjects:
        with open(f"./_datasets/news400/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()

def createSingleEntityQuestions(args):
    with open(f"./_datasets/news400/news400_merged.jsonl", 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            # person, location, event
            for entityObject in entityObjects:
                if lineObject[entityObject['label']] == 1:

                    baseQuestion = "\"Does the two images show the same {} ?\""

                    # text entites
                    if 'untampered' in lineObject['test_' + entityObject['name']]:
                        for entityID in lineObject['test_' + entityObject['name']]['untampered']:
                            if entityObject['name'] == "locations":
                                entityFiles = glob.glob(f"/nfs/data/image_repurposing/News400/reference_images/wd_PLACES/{entityID}/google_*.jpg")
                            else:
                                entityFiles = glob.glob(f"/nfs/data/image_repurposing/News400/reference_images/wd_{str(entityObject['name']).upper()}/{entityID}/google_*.jpg")
                            
                            if len(entityFiles) == 0:
                                continue

                            news_image = f"./_datasets/news400/images/{str(lineObject['id'])}.png"
                            entity_image = entityFiles[0]

                            question = baseQuestion.format(entityObject['name'][:-1])#, extractNameById(entityID, entityObject['entities']))
                            # text entites (validated visible)
                            if 'visible' in lineObject['test_' + entityObject['name']]:
                                if entityID in lineObject['test_' + entityObject['name']]['visible']:
                                    saveQuestion(args, str(lineObject['id']), str(news_image), str(entity_image), str(question), str(entityObject['name']), "orginal", "text", entityID, "yes", "no")
                                else:
                                    saveQuestion(args, str(lineObject['id']), str(news_image), str(entity_image), str(question), str(entityObject['name']), "orginal", "text", entityID, "no", "yes")
                            else:
                                saveQuestion(args, str(lineObject['id']), str(news_image), str(entity_image), str(question), str(entityObject['name']), "orginal", "text", entityID, "no", "yes")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def saveQuestion(args, id, news_image, entity_image, question, entity, testlabel, set, entityID, ground_truth, ground_wrong):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"news_image\": \"%s\", \"entity_image\": \"%s\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"entityID\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, news_image, entity_image, question, entity, testlabel, set, entityID, ground_truth, ground_wrong))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--base-path", type=str, default="")
    args = parser.parse_args()

    open(args.question_file, 'w').close()

    # load entity datasets
    loadEntities()

    # create Questions
    createSingleEntityQuestions(args)