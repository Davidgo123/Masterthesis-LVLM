import json
import random
import argparse

subsample_datasets= [
    {
        "name": "persons",
        "path": "/nfs/home/ernstd/data/news400/subsamples/news400_persons.jsonl",
        "label": "annotation_persons",
        "entities": [],
        "test_labels": ["random", "gender-sensitive", "country-sensitive", "country-gender-sensitive"] 
    },
    {
        "name": "locations",
        "path": "/nfs/home/ernstd/data/news400/subsamples/news400_locations.jsonl",
        "label": "annotation_locations",
        "entities": [],
        "test_labels": ["random", "country-continent", "region-country", "city-region"] 
    },
    {
        "name": "events",
        "path": "/nfs/home/ernstd/data/news400/subsamples/news400_events.jsonl",
        "label": "annotation_events",
        "entities": [],
        "test_labels": ["random", "same_instance"]
    }
]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def createSubSamples():
    # delete existing files
    for subsample in subsample_datasets:
        open(subsample['path'], 'w').close()

    # run trough dataset
    with open('/nfs/home/ernstd/data/news400/news400.jsonl', 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)
            # append content to subsample
            for subsample in subsample_datasets:
                if (lineObject[subsample['label']] == 1):
                    with open(subsample['path'], "a") as outfile:
                        outfile.write(json.dumps(lineObject) + "\n")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def loadEntityDatasets():
    for subsample in subsample_datasets:
        with open(f"/nfs/home/ernstd/data/news400/entities/{subsample['name']}.jsonl", 'r') as file:
            for line in file:
                subsample['entities'].append(json.loads(line))



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def extractNames(lineObject, entityDataset, entityLabel, entityLabelTest, test_label):
    # extract ids for entity type
    real_entity_ids = []
    fake_entity_ids = []

    if lineObject[entityLabel]:
        for entity in lineObject[entityLabel]: 
            real_entity_ids.append(entity['wd_id'])

    if test_label in lineObject[entityLabelTest]:
        for entity in lineObject[entityLabelTest][test_label]:
            fake_entity_ids.append(entity)

    # extract labels for entity type
    real_entity_names = []
    fake_entity_names = []
    for entity in entityDataset:
        if entity['wd_id'] in real_entity_ids:
            real_entity_names.append(str(entity['wd_label']).replace("\"", "'").replace("'", "").lower())
        
        if entity['wd_id'] in fake_entity_ids:
            fake_entity_names.append(str(entity['wd_label']).replace("\"", "'").replace("'", "").lower())

    return {"text": real_entity_names, "test": fake_entity_names}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    
def createMultiLabelQuestions(args):
    # run trough dataset
    with open('/nfs/home/ernstd/data/news400/news400.jsonl', 'r') as file:
        for line in file:
            
            # extract line
            lineObject = json.loads(line)

            # entity ids
            entities = {
                "persons": extractNames(lineObject, subsample_datasets[0]['entities'], "text_persons", "test_persons", "random"),
                "locations": extractNames(lineObject, subsample_datasets[1]['entities'], "text_locations", "test_locations", "random"),
                "events": extractNames(lineObject, subsample_datasets[2]['entities'], "text_events", "test_events", "random")
            }

            #randomize truth and test entities in question
            baseQuestion = "\"Which set of entities is more consistent to the image? Information about the entity sets: A=[{}-({}), {}-({}), {}-({})] or B=[{}-({}), {}-({}), {}-({})].\""
            if random.randint(0,1) == 1:
                question = baseQuestion.format(
                                list(entities.keys())[0], ','.join(entities["persons"]["text"]), list(entities.keys())[1], ','.join(entities["locations"]["text"]), list(entities.keys())[2], ','.join(entities["events"]["text"]),
                                list(entities.keys())[0], ','.join(entities["persons"]["test"]), list(entities.keys())[1], ','.join(entities["locations"]["test"]), list(entities.keys())[2], ','.join(entities["events"]["test"]),
                            )
                saveQuestion(args, str(lineObject['id']), "multiLabel", "multi", "random", str(question), "A", "B")

            else:
                question = baseQuestion.format(
                                list(entities.keys())[0], ','.join(entities["persons"]["test"]), list(entities.keys())[1], ','.join(entities["locations"]["test"]), list(entities.keys())[2], ','.join(entities["events"]["test"]),
                                list(entities.keys())[0], ','.join(entities["persons"]["text"]), list(entities.keys())[1], ','.join(entities["locations"]["text"]), list(entities.keys())[2], ','.join(entities["events"]["text"]),
                            )
                saveQuestion(args, str(lineObject['id']), "multiLabel", "multi", "random", str(question), "B", "A")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createPairLabelQuestions(args):
    for subsample in subsample_datasets:
        with open(subsample['path'], 'r') as file:
            for line in file:
                # extract line
                lineObject = json.loads(line)

                for test_label in subsample['test_labels']:
                    entities = extractNames(lineObject, subsample['entities'], "text_" + subsample['name'], "test_" + subsample['name'], test_label)

                    #randomize truth and test entities in question
                    baseQuestion = "\"Which set of {} is more consistent to the image: A=({}) or B=({})?\""
                    if random.randint(0,1) == 1:
                        question = baseQuestion.format(subsample['name'], ','.join(entities["text"]), ','.join(entities["test"]))
                        saveQuestion(args, str(lineObject['id']), "pairLabel", subsample['name'], test_label, str(question), "A", "B")

                    else:
                        question = baseQuestion.format(subsample['name'], ','.join(entities["test"]), ','.join(entities["text"]))
                        saveQuestion(args, str(lineObject['id']), "pairLabel", subsample['name'], test_label, str(question), "B", "A")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createPairEntityQuestions(args):
    for subsample in subsample_datasets:
        with open(subsample['path'], 'r') as file:
            for line in file:
                # extract line
                lineObject = json.loads(line)

                for test_label in subsample['test_labels']:
                    entities = extractNames(lineObject, subsample['entities'], "text_" + subsample['name'], "test_" + subsample['name'], test_label)

                    #randomize truth and test entities in question
                    baseQuestion = "\"Which {} is more consistent to the image: A=({}) or B=({})?\""
                    for i in range(len(entities["text"])):
                        if random.randint(0,1) == 1:
                            question = baseQuestion.format(subsample['name'][:-1], entities["text"][i], entities["test"][i])
                            saveQuestion(args, str(lineObject['id']), "pairEntity", subsample['name'], test_label, str(question), "A", "B")

                        else:
                            question = baseQuestion.format(subsample['name'][:-1], entities["test"][i], entities["text"][i])
                            saveQuestion(args, str(lineObject['id']), "pairEntity", subsample['name'], test_label, str(question), "B", "A")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def createSingleEntityQuestions(args):
    for subsample in subsample_datasets:
        with open(subsample['path'], 'r') as file:
            for line in file:
                # extract line
                lineObject = json.loads(line)

                for test_label in subsample['test_labels']:
                    entities = extractNames(lineObject, subsample['entities'], "text_" + subsample['name'], "test_" + subsample['name'], test_label)

                    baseQuestion = "\"Is the {} '{}' consistent to the image?\""
                    for entity in entities["text"]:
                        question = baseQuestion.format(subsample['name'][:-1], entity)
                        saveQuestion(args, str(lineObject['id']), "singleEntity", subsample['name'], test_label, str(question), "yes", "no")
                    
                    for entity in entities["test"]:
                        question = baseQuestion.format(subsample['name'][:-1], entity)
                        saveQuestion(args, str(lineObject['id']), "singleEntity", subsample['name'], test_label, str(question), "no", "yes")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def createGolsaLocationQuestions(args):
    subsample_datasets
    with open('/nfs/home/ernstd/data/golsa/golsa.jsonl', 'r') as file:
        for line in file:
            # extract line
            lineObject = json.loads(line)
            print(lineObject)
            randName = random.choice(subsample_datasets[1]['entities'])['wd_label']
            print(randName)

            realName=""
            for entity in subsample_datasets[1]['entities']:
                if entity['wd_id'] == lineObject['image_label']['city']['id']:
                    realName = entity['wd_label']                

            #randomize truth and test entities in question
            baseQuestion = "\"Which {} is more consistent to the image: A=({}) or B=({})?\""
            if random.randint(0,1) == 1:
                question = baseQuestion.format('location', realName, randName)
                saveQuestionGolsa(args, str(lineObject['id']), "singleEntity", 'locations', 'random', str(question), "A", "B")

            else:
                question = baseQuestion.format('location', randName, realName)
                saveQuestionGolsa(args, str(lineObject['id']), "singleEntity", 'locations', 'random', str(question), "B", "A")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def saveQuestionGolsa(args, id, questionType, entity, category, question, truth_label, wrong_label):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"questionType\": \"%s\", \"image\": \"/nfs/home/ernstd/data/golsa/images/%s.jpg\", \"text\": %s, \"entity\": \"%s\", \"category\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\"}\n""" % (id, questionType, id, question, entity, category, truth_label, wrong_label))


def saveQuestion(args, id, questionType, entity, category, question, truth_label, wrong_label):
    with open(args.question_file, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"questionType\": \"%s\", \"image\": \"/nfs/home/ernstd/data/news400/images/%s.png\", \"text\": %s, \"entity\": \"%s\", \"category\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\"}\n""" % (id, questionType, id, question, entity, category, truth_label, wrong_label))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    parser = argparse.ArgumentParser()
    parser.add_argument("--question-file", type=str, default="")
    args = parser.parse_args()

    open(args.question_file, 'w').close()

    # create subsamples from news400 for each entity
    createSubSamples()

    # load entity datasets
    loadEntityDatasets()

    #createMultiLabelQuestions(args)
    #createPairLabelQuestions(args)
    #createPairEntityQuestions(args)
    #createSingleEntityQuestions(args)
    createGolsaLocationQuestions(args)

