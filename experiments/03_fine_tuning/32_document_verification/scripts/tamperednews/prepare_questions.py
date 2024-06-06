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
        with open(f"./_datasets/tamperednews/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()

def createSingleEntityQuestions(args):
    with open(f"./_datasets/tamperednews/tamperednews.jsonl", 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            # person, location, event
            for entityObject in entityObjects:
                if lineObject[entityObject['label']] == 1:

                    # random, ...
                    for testLabel in entityObject['test_labels']:
                        if testLabel in lineObject['test_' + entityObject['name']]:
                            # text entites
                            if 'untampered' in lineObject['test_' + entityObject['name']]:

                                # multi entity questions
                                if "Decide" in args.prompt:
                                    createMultiEntityQuestions(args, lineObject, entityObject, testLabel)
                                    continue
                                    
                                # single entity questions
                                for entityID in lineObject['test_' + entityObject['name']]['untampered']:
                                    question = args.prompt.replace("<type>", entityObject['name'][:-1])
                                    orgID = extractNameById(entityID, entityObject['entities'])
                                    if not orgID:
                                        continue
                                    question = question.replace("<name>", orgID)
                                    # text entites (validated visible)
                                    if 'visible' in lineObject['test_' + entityObject['name']]:
                                        if entityID in lineObject['test_' + entityObject['name']]['visible']:
                                            saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", entityID, "yes", "no")
                                        else:
                                            saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", entityID, "no", "yes")
                                    else:
                                        saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "text", entityID, "no", "yes")
                            
                            # test entites
                            for entityID in lineObject['test_' + entityObject['name']][testLabel]:
                                question = args.prompt.replace("<type>", entityObject['name'][:-1])
                                orgID = extractNameById(entityID, entityObject['entities'])
                                if not orgID:
                                    continue
                                question = question.replace("<name>", orgID)
                                saveQuestion(args, str(lineObject['id']), str(question), entityObject['name'], testLabel, "test", entityID, "no", "yes")



def createMultiEntityQuestions(args, lineObject, entityObject, testLabel):
    orginalEntityIDs = [] 
    visibleEntityIDs = []
    tamperedEntityIDs = []

    for entityID in lineObject['test_' + entityObject['name']]['untampered']:
        orginalEntityIDs.append(entityID)
        if 'visible' in lineObject['test_' + entityObject['name']]:
            if entityID in lineObject['test_' + entityObject['name']]['visible']:
                visibleEntityIDs.append(entityID)            
    
    for entityID in lineObject['test_' + entityObject['name']][testLabel]:
        tamperedEntityIDs.append(entityID)

    if visibleEntityIDs and tamperedEntityIDs:
        if "name1" in args.prompt:
            for visibleEntity in visibleEntityIDs:
                index = orginalEntityIDs.index(visibleEntity)
                
                if index >= len(tamperedEntityIDs):
                    continue

                question = args.prompt.replace("<type>", entityObject['name'][:-1])
                orgID = extractNameById(orginalEntityIDs[index], entityObject['entities'])
                tampID = extractNameById(tamperedEntityIDs[index], entityObject['entities'])
                
                if not orgID or not tampID:
                    continue

                if (random.randint(0,1) == 0):
                    question = question.replace("<name1>", orgID)
                    question = question.replace("<name2>", tampID)
                    saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "-", entityID, "A", "B")
                else:
                    question = question.replace("<name1>", tampID)
                    question = question.replace("<name2>", orgID)
                    saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "-", entityID, "B", "A")

        elif "set1" in args.prompt:
            indices = []
            for visibleEntity in visibleEntityIDs:
                indices.append(orginalEntityIDs.index(visibleEntity))

            if max(indices) >= len(tamperedEntityIDs):
                return

            question = args.prompt.replace("<types>", entityObject['name'])
            orgIDs = str([extractNameById(orginalEntityIDs[i], entityObject['entities']) for i in indices])
            tampIDs = str([extractNameById(tamperedEntityIDs[i], entityObject['entities']) for i in indices])

            if not orgIDs or not tampIDs:
                return
            
            if (random.randint(0,1) == 0):
                question = question.replace("<set1>", orgIDs)
                question = question.replace("<set2>", tampIDs)
                saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "-", entityID, "A", "B")
            else:
                question = question.replace("<set1>", tampIDs)
                question = question.replace("<set2>", orgIDs)
                saveQuestion(args, str(lineObject['id']), str(question), str(entityObject['name']), str(testLabel), "-", entityID, "B", "A")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def saveQuestion(args, id, question, entity, testlabel, set, entityID, ground_truth, ground_wrong):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"./_datasets/tamperednews/images/%s.jpg\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"entityID\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, id, question, entity, testlabel, set, entityID, ground_truth, ground_wrong))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--base-path", type=str, default="")
    parser.add_argument("--prompt", type=str, default="")
    args = parser.parse_args()

    open(args.question_file, 'w').close()

    # load entity datasets
    loadEntities()

    # create Questions
    createSingleEntityQuestions(args)