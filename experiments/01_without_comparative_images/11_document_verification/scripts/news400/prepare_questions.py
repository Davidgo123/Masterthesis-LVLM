import json
import random
import argparse

entityObjects = [
    {
        "name": "persons",
        "label": "annotation_persons",
        "entities": [],
        "test_labels": ["random", "gender-sensitive", "country-sensitive", "country-gender-sensitive"] 
    },
    {
        "name": "locations",
        "label": "annotation_locations",
        "entities": [],
        "test_labels": ["random", "country-continent", "region-country", "city-region"] 
    },
    {
        "name": "events",
        "label": "annotation_events",
        "entities": [],
        "test_labels": ["random", "same_instance"]
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

                    baseQuestion = "\"Is the {} {} visible in this photo ?\""

                    # random, ...
                    for testLabel in entityObject['test_labels']:
                        if testLabel in lineObject['test_' + entityObject['name']]:
                            # text entites
                            if 'untampered' in lineObject['test_' + entityObject['name']]:
                                for entityID in lineObject['test_' + entityObject['name']]['untampered']:
                                    question = baseQuestion.format(entityObject['name'][:-1], extractNameById(entityID, entityObject['entities']))
                                    # text entites (validated visible)
                                    if 'visible' in lineObject['test_' + entityObject['name']]:
                                        if entityID in lineObject['test_' + entityObject['name']]['visible']:
                                            saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", "yes", "no")
                                        else:
                                            saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", "no", "yes")
                                    else:
                                        saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", "no", "yes")
                            
                            # test entites
                            for entityID in lineObject['test_' + entityObject['name']][testLabel]:
                                question = baseQuestion.format(entityObject['name'][:-1], extractNameById(entityID, entityObject['entities']))
                                saveQuestion(args, str(lineObject['id']), str(question), entityObject['name'], testLabel, "test", "no", "yes")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def saveQuestion(args, id, question, entity, testlabel, set, ground_truth, ground_wrong):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"./_datasets/news400/images/%s.png\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, id, question, entity, testlabel, set, ground_truth, ground_wrong))


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