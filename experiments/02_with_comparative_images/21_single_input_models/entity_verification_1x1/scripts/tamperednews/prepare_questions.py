import json
import random
import argparse
from PIL import Image, ImageDraw, ImageFilter
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
        with open(f"./_datasets/tamperednews/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def generate1x1Image(newsImage, entityImage, questionID, entityID):
    
    newsImage = Image.open(newsImage)
    entityImage = Image.open(entityImage)

    w_1, h_1 = newsImage.size
    w_2, h_2 = entityImage.size

    # newsImage is landscape (top/bot split)
    if w_1 > h_1:
        # scale width
        scale_factor = w_1 / w_2
        scaled_height = int(h_2 * scale_factor)
        entityImage = entityImage.resize((w_1, scaled_height))
        w_2, h_2 = entityImage.size

        # rescale height if newsImage is landscape and entityImage portrait
        if h_1 * 1.5 < h_2:
            scale_factor = h_1 / h_2
            scaled_width = int(w_2 * scale_factor)
            entityImage = entityImage.resize((int(scaled_width * 1.3), int(h_1 * 1.3)))
            w_2, h_2 = entityImage.size

        # create combined image with colored background
        w_max = int(1.1 * w_1)
        h_max = int(1.1 * h_1 + 1.1 * h_2)
        combinedImage = Image.new("RGB", (w_max, h_max))
        shape = [[(0, 0), (w_max, h_max)], [(0, 1.1 * h_1), (w_max, h_max)]]
        drawer = ImageDraw.Draw(combinedImage)   
        drawer.rectangle(shape[0], fill ="red") 
        drawer.rectangle(shape[1], fill ="blue") 
        combinedImage.paste(newsImage, (int(w_max * 0.05), int(h_max * 0.025)))
        combinedImage.paste(entityImage, (int((w_max - w_2) / 2), int(1.1 * h_1 + 0.05 * h_2)))
        combinedImage.save(f"{args.base_path}/images/tamperednews/{questionID}_{entityID}.jpg", quality=95)    
    
    # newsImage is portrait (left/right split)
    else:
        # scale height
        scale_factor = h_1 / h_2
        scaled_width = int(w_2 * scale_factor)
        entityImage = entityImage.resize((scaled_width, h_1))
        w_2, h_2 = entityImage.size

        # rescale width if newsImage is portrait and entityImage landscape
        if w_1 * 1.5 < w_2:
            scale_factor = w_1 / w_2
            scaled_height = int(h_2 * scale_factor)
            entityImage = entityImage.resize((int(w_1 * 1.3), int(scaled_height * 1.3)))
            w_2, h_2 = entityImage.size

        # create combined image with colored background
        w_max = int(1.1 * w_1 + 1.1 * w_2)
        h_max = int(1.1 * h_1)
        combinedImage = Image.new("RGB", (w_max, h_max))
        shape = [[(0, 0), (w_max, h_max)], [(1.1 * w_1, 0), (w_max, h_max)]]
        drawer = ImageDraw.Draw(combinedImage)   
        drawer.rectangle(shape[0], fill ="red") 
        drawer.rectangle(shape[1], fill ="blue") 
        combinedImage.paste(newsImage, (int(w_max * 0.025), int(h_max * 0.05)))
        combinedImage.paste(entityImage, (int(1.1 * w_1 + 0.05 * w_2), int((h_max - h_2) / 2)))
        combinedImage.save(f"{args.base_path}/images/tamperednews/{questionID}_{entityID}.jpg", quality=95)

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

                    baseQuestion = "\"Does the red part of the image show the same {} as the blue part of the image ?\""

                    # text entites
                    if 'untampered' in lineObject['test_' + entityObject['name']]:
                        for entityID in lineObject['test_' + entityObject['name']]['untampered']:
                            if entityObject['name'] == "locations":
                                entityFiles = glob.glob(f"/nfs/data/image_repurposing/BreakingNews/reference_images/wd_PLACES/{entityID}/google_*.jpg")
                            else:
                                entityFiles = glob.glob(f"/nfs/data/image_repurposing/BreakingNews/reference_images/wd_{str(entityObject['name']).upper()}/{entityID}/google_*.jpg")
                            
                            if len(entityFiles) > 0:
                                generate1x1Image(f"./_datasets/tamperednews/images/{str(lineObject['id'])}.jpg", entityFiles[0], str(lineObject['id']), str(entityID))
                            else:
                                continue

                            question = baseQuestion.format(entityObject['name'][:-1])#, extractNameById(entityID, entityObject['entities']))
                            # text entites (validated visible)
                            if 'visible' in lineObject['test_' + entityObject['name']]:
                                if entityID in lineObject['test_' + entityObject['name']]['visible']:
                                    saveQuestion(args, str(lineObject['id']), str(entityID), str(question), str(entityObject['name']), "orginal", "text", "yes", "no")
                                else:
                                    saveQuestion(args, str(lineObject['id']), str(entityID), str(question), str(entityObject['name']), "orginal", "text", "no", "yes")
                            else:
                                saveQuestion(args, str(lineObject['id']), str(entityID), str(question), str(entityObject['name']), "orginal", "text", "no", "yes")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def saveQuestion(args, id, entityID, question, entity, testlabel, set, ground_truth, ground_wrong):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s/images/tamperednews/%s_%s.jpg\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, args.base_path, id, entityID, question, entity, testlabel, set, ground_truth, ground_wrong))


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