import json
import random

pathQuestions = "/nfs/home/ernstd/data/news400/document_verification/multi_entity/questions.jsonl"

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

def createQuestionsForSingleEntityType():
    for subsample in subsample_datasets:
        with open(subsample['path'], 'r') as file:
            for line in file:
                # extract line
                lineObject = json.loads(line)

                for test_label in subsample['test_labels']:
                    entities = extractNames(lineObject, subsample['entities'], "text_" + subsample['name'], "test_" + subsample['name'], test_label)

                    #randomize truth and test entities in question
                    if random.randint(0,1) == 1:
                        question = ("""\"Decide which set of entities is more consistent to the image. Information about the given entity sets: A=%s - (%s), B=%s - (%s). Answer only with A or B.\"""" % (
                                    subsample['name'], ','.join(entities["text"]),
                                    subsample['name'], ','.join(entities["test"])
                                    ))
                        saveQuestion(str(lineObject['id']), subsample['name'], test_label, str(question), "A", "B")

                    else:
                        question = ("""\"Decide which set of entities is more consistent to the image. Information about the given entity sets: A=%s - (%s), B=%s - (%s). Answer only with A or B.\"""" % (
                                    subsample['name'], ','.join(entities["test"]),
                                    subsample['name'], ','.join(entities["text"])
                                    ))
                        saveQuestion(str(lineObject['id']), subsample['name'], test_label, str(question), "B", "A")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    
def createQuestionsForAllEntityTypes():
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

            if random.randint(0,1) == 1:
                question = ("""\"Decide which set of entities is more consistent to the image. Information about the given entity sets: A=[%s - (%s), %s - (%s), %s - (%s)], B=[%s - (%s), %s - (%s), %s - (%s)]. Answer only with A or B.\"""" % (
                            list(entities.keys())[0], ','.join(entities["persons"]["text"]), list(entities.keys())[1], ','.join(entities["locations"]["text"]), list(entities.keys())[2], ','.join(entities["events"]["text"]),
                            list(entities.keys())[0], ','.join(entities["persons"]["test"]), list(entities.keys())[1], ','.join(entities["locations"]["test"]), list(entities.keys())[2], ','.join(entities["events"]["test"]),
                            ))
                saveQuestion(str(lineObject['id']), "multi", "random", str(question), "A", "B")

            else:
                question = ("""\"Decide which set of entities is more consistent to the image. Information about the given entity sets: A=[%s - (%s), %s - (%s), %s - (%s)], B=[%s - (%s), %s - (%s), %s - (%s)]. Answer only with A or B.\"""" % (
                            list(entities.keys())[0], ','.join(entities["persons"]["test"]), list(entities.keys())[1], ','.join(entities["locations"]["test"]), list(entities.keys())[2], ','.join(entities["events"]["test"]),
                            list(entities.keys())[0], ','.join(entities["persons"]["text"]), list(entities.keys())[1], ','.join(entities["locations"]["text"]), list(entities.keys())[2], ','.join(entities["events"]["text"]),
                            ))
                saveQuestion(str(lineObject['id']), "multi", "random", str(question), "B", "A")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def saveQuestion(id, entity, category, question, truth_label, wrong_label):
    with open(pathQuestions, "a") as outfile:
        outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s.png\", \"text\": %s, \"entity\": \"%s\", \"category\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\"}\n""" % (id, id, question, entity, category, truth_label, wrong_label))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    # delete questions
    open(pathQuestions, 'w').close()

    # create subsamples from news400 for each entity
    createSubSamples()

    # load entity datasets
    loadEntityDatasets()

    createQuestionsForSingleEntityType()
    createQuestionsForAllEntityTypes()


