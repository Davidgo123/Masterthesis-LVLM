import json
import random
import argparse
import geopy.distance
import numpy
import shutil

subsample_dataset = {
        "name": "locations",
        "path": "/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl",
        "entities": [],
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
    open('/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl', 'w').close()
    with open('/nfs/home/ernstd/data/mmg/test_dataset.json', 'r') as f:
        data = json.load(f)

    rng = numpy.random.default_rng()
    randomRows = rng.choice(len(list(data['city'].keys())), size=100, replace=False)

    with open('/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl', 'a') as f:
        for i in randomRows:
            keyIndex = list(data['city'].keys())[i]
            del data['city'][keyIndex]['body']
            f.write(json.dumps(data['city'][keyIndex]) + "\n")
            id = data['city'][keyIndex]['id']
            shutil.copyfile(f'/nfs/home/tahmasebzadehg/mmg_news_dataset/image_splits/test/{id}.jpg', f'/nfs/home/ernstd/data/mmg/images/{id}.jpg')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def loadEntityDatasets():
    with open(f"/nfs/home/ernstd/data/news400/entities/{subsample_dataset['name']}.jsonl", 'r') as file:
        for line in file:
            subsample_dataset['entities'].append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNameById(data_list, id):
    for entity in data_list:
        if entity['wd_id'] == id:
            return entity['wd_label']
        
def getTamperedIDByInstance(data_list, instance, category, truth_id):
    filtered_data = [data for data in data_list if "instance" in data.get("meta_tags", {}) and instance in data["meta_tags"]["instance"]]
    random.shuffle(filtered_data)
    for item in filtered_data:
        if checkDistanze(data_list, truth_id, item['wd_id'], category):
            return item['wd_id']
    return random.choice(filtered_data)['wd_id']

def checkDistanze(data_list, truth_id, tampered_id, category):
    truth_entity = {}
    tampered_entity = {}

    for entity in data_list:
        if entity['wd_id'] == truth_id:
            truth_entity = entity
        if entity['wd_id'] == tampered_id:
            tampered_entity = entity
        
    dis = geopy.distance.geodesic((truth_entity['latitude'], truth_entity['longitude']), (tampered_entity['latitude'], tampered_entity['longitude'])).km
    if (dis > distanzes[category]['minDis'] and dis < distanzes[category]['maxDis']):
        return True
    else:
        return False

def extractNames(lineObject, category):
    types = ['city', 'country', 'continent']
    realNames=[]
    randNames=[]

    for type in types:
        realName = extractNameById(subsample_dataset['entities'], lineObject['image_label'][type]['id'])
        if realName != None:
            realNames.append(realName)
            randNames.append(extractNameById(subsample_dataset['entities'], getTamperedIDByInstance(subsample_dataset['entities'], type, category, lineObject['image_label'][type]['id'])))

    return {"text": realNames, "test": randNames}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createPairLabelQuestions(args):
    with open('/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl', 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            for category in subsample_dataset['test_labels']:
                names = extractNames(lineObject, category)

                #randomize truth and test entities in question
                baseQuestion = "\"Which set of {} is more consistent to the image: A=({}) or B=({})?\""
                if random.randint(0,1) == 1:
                    question = baseQuestion.format(subsample_dataset['name'], ','.join(names["text"]), ','.join(names["test"]))
                    saveQuestion(args, str(lineObject['id']), "pairLabel", subsample_dataset['name'], category, str(question), "A", "B")

                else:
                    question = baseQuestion.format(subsample_dataset['name'], ','.join(names["test"]), ','.join(names["text"]))
                    saveQuestion(args, str(lineObject['id']), "pairLabel", subsample_dataset['name'], category, str(question), "B", "A")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createPairEntityQuestions(args):
    with open('/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl', 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            for category in subsample_dataset['test_labels']:
                names = extractNames(lineObject, category)

                #randomize truth and test entities in question
                baseQuestion = "\"Which {} is more consistent to the image: A=({}) or B=({})?\""
                for i in range(len(names["text"])):
                    if random.randint(0,1) == 1:
                        question = baseQuestion.format(subsample_dataset['name'], names["text"][i], names["test"][i])
                        saveQuestion(args, str(lineObject['id']), "pairLabel", subsample_dataset['name'], category, str(question), "A", "B")

                    else:
                        question = baseQuestion.format(subsample_dataset['name'], names["test"][i], names["text"][i])
                        saveQuestion(args, str(lineObject['id']), "pairLabel", subsample_dataset['name'], category, str(question), "B", "A")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createSingleEntityQuestions(args):
    with open('/nfs/home/ernstd/data/mmg/subsamples/mmg_locations.jsonl', 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)

            for category in subsample_dataset['test_labels']:
                names = extractNames(lineObject, category)

                #randomize truth and test entities in question
                baseQuestion = "\"Is the {} '{}' consistent to the image?\""
                for entity in names["text"]:
                    question = baseQuestion.format(subsample_dataset['name'], entity)
                    saveQuestion(args, str(lineObject['id']), "singleEntity", subsample_dataset['name'], category, str(question), "yes", "no")

                for entity in names["test"]:
                    question = baseQuestion.format(subsample_dataset['name'], entity)
                    saveQuestion(args, str(lineObject['id']), "singleEntity", subsample_dataset['name'], category, str(question), "no", "yes")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def saveQuestion(args, id, questionType, entity, category, question, truth_label, wrong_label):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"questionType\": \"%s\", \"image\": \"/nfs/home/ernstd/data/mmg/images/%s.jpg\", \"text\": %s, \"entity\": \"%s\", \"category\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\"}\n""" % (id, questionType, id, question, entity, category, truth_label, wrong_label))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    args = parser.parse_args()

    # create new subsample from mmg dataset
    #createSubSample()

    # load entity datasets
    loadEntityDatasets()

    createPairLabelQuestions(args)
    createPairEntityQuestions(args)
    createSingleEntityQuestions(args)

