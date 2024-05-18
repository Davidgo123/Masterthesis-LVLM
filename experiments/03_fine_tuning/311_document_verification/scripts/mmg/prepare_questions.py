import json
import random
import argparse
import geopy.distance
import numpy
import shutil

entityObject = {
        "name": "locations",
        "path": "./_datasets/mmg/subsamples/mmg_locations.jsonl",
        "entities": [],
        "text_labels": ["city", "country", "continent"],
        "test_labels": ["random", "country-continent", "region-country", "city-region"] 
    }

distanzes = {
    "random": {
        "minDis": 0,
        "maxDis": 999999
    },
    "country-continent": {
        "minDis": 2500,
        "maxDis": 750
    },
    "region-country": {
        "minDis": 750,
        "maxDis": 200
    },
    "city-region": {
        "minDis": 200,
        "maxDis": 25
    },
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def createSubSample():
    open(entityObject['path'], 'w').close()

    with open('./_datasets/mmg/test_dataset.json', 'r') as f:
        data = json.load(f)

    rng = numpy.random.default_rng()
    randomRows = rng.choice(len(list(data['city'].keys())), size=200, replace=False)

    with open(entityObject['path'], 'a') as f:
        for i in randomRows:
            keyIndex = list(data['city'].keys())[i]
            del data['city'][keyIndex]['body']
            f.write(json.dumps(data['city'][keyIndex]) + "\n")
            id = data['city'][keyIndex]['id']
            shutil.copyfile(f'/nfs/home/tahmasebzadehg/mmg_news_dataset/image_splits/test/{id}.jpg', f'./_datasets/mmg/images/{id}.jpg')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
def checkDistanze(data_list, testLabel, entityID, tampered_id):
    truth_entity = {}
    tampered_entity = {}

    for entity in data_list:
        if entity['wd_id'] == entityID:
            truth_entity = entity
        if entity['wd_id'] == tampered_id:
            tampered_entity = entity
        
    dis = geopy.distance.geodesic((truth_entity['latitude'], truth_entity['longitude']), (tampered_entity['latitude'], tampered_entity['longitude'])).km
    if (dis > distanzes[testLabel]['minDis'] and dis < distanzes[testLabel]['maxDis']):
        return True
    else:
        return False

def getTamperedIDByInstance(data_list, instance, testLabel, entityID):
    filtered_data = [data for data in data_list if "instance" in data.get("meta_tags", {}) and instance in data["meta_tags"]["instance"]]
    random.shuffle(filtered_data)
    for item in filtered_data:
        if checkDistanze(data_list, testLabel, entityID, item['wd_id']):
            return item['wd_id']
    return random.choice(filtered_data)['wd_id']

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def loadEntities():
    with open(f"./_datasets/news400/entities/{entityObject['name']}.jsonl", 'r') as file:
        for line in file:
            entityObject['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()

def createSingleEntityQuestions(args):
    with open(entityObject['path'], 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            baseQuestion = "\"Is the {} {} visible in this photo ?\""

            # city, country, continent
            for instance in entityObject['text_labels']:

                entityID = lineObject['image_label'][instance]['id']
                if extractNameById(entityID, entityObject['entities']) == None:
                    continue
                
                # random, ... 
                for testLabel in entityObject['test_labels']:                    
                    # save untampered question
                    question = baseQuestion.format(instance, extractNameById(entityID, entityObject['entities']))
                    saveQuestion(args, str(lineObject['id']), str(question), str(instance), str(testLabel), "text", str(entityID), "yes", "no")

                    # save tampered question 
                    tamperedEntityID = getTamperedIDByInstance(entityObject['entities'], instance, testLabel, entityID)
                    entity = extractNameById(tamperedEntityID, entityObject['entities'])
                    question = baseQuestion.format(instance, entity)
                    saveQuestion(args, str(lineObject['id']), str(question), str(instance), str(testLabel), "test", str(tamperedEntityID), "no", "yes")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def saveQuestion(args, id, question, entity, testlabel, set, entityID, ground_truth, ground_wrong):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"./_datasets/mmg/images/%s.jpg\", \"question\": %s, \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"entityID\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\"} \n""" 
                      % (id, id, question, entity, testlabel, set, entityID, ground_truth, ground_wrong))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--base-path", type=str, default="")
    args = parser.parse_args()

    # create new subsample from mmg dataset
    #createSubSample()

    open(args.question_file, 'w').close()

    # load entity datasets
    loadEntities()

    # create Questions
    createSingleEntityQuestions(args)

