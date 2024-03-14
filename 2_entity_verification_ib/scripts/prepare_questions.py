import json
import random
import argparse
from PIL import Image, ImageDraw, ImageFilter

entityObjects = [
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
        with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/news400/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# todo
def createMultiImage():
    template_1_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/template.png')
    img_untampered = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/1.png').resize((750, 533))
    img_tampered_1 = Image.open('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/2.png').resize((750, 533)) #(350, 250)     
    template_1_1.paste(img_untampered, (25, 33))
    template_1_1.paste(img_tampered_1, (825, 33)) #(825, 317), (1225, 33), (1225, 317)

    template_1_1.save('/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/template_1_filled.png', quality=95)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()

def createSingleEntityQuestions(args):
    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/news400/news400_merged.jsonl", 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            # location, event
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
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"/nfs/home/ernstd/masterthesis_scripts/_datasets/news400/images/%s.png\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, id, question, entity, testlabel, set, ground_truth, ground_wrong))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    args = parser.parse_args()

    open(args.question_file, 'w').close()

    # load entity datasets
    loadEntities()

    # create Questions
    createSingleEntityQuestions(args)