import json

datasets = [
    "news400/news400_merged.jsonl",
    "tamperednews/tamperednews.jsonl",
    "mmg/subsamples/mmg_locations.jsonl"
]

def count(dataset):
    
    # persons, locations, events
    countedDocuments = {
        "persons": 0,
        "locations": 0,
        "events": 0,
    }

    countedEntities = {
        "persons": [],
        "locations": [],
        "events": [],
    }

    visibleEntities = {
        "persons": [],
        "locations": [],
        "events": [],
    }

    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/{dataset}", 'r') as f:
        for line in f:
            lineObject = json.loads(line)

            # mmg
            if "mmg" in dataset:
                if "image_label" in lineObject:
                    countedDocuments["locations"] = countedDocuments["locations"] + 1
                    if "city" in lineObject["image_label"]:
                        if lineObject["image_label"]["city"]["id"] not in countedEntities["persons"]:
                            countedEntities["persons"].append(lineObject["image_label"]["city"]["id"])
                    if "country" in lineObject["image_label"]:
                        if lineObject["image_label"]["country"]["id"] not in countedEntities["locations"]:
                            countedEntities["locations"].append(lineObject["image_label"]["country"]["id"])
                    if "continent" in lineObject["image_label"]:
                        if lineObject["image_label"]["continent"]["id"] not in countedEntities["events"]:
                            countedEntities["events"].append(lineObject["image_label"]["continent"]["id"])

            # enws400, tamperedNews
            else:
                entities = ["persons", "locations", "events"]
                for entity in entities:
                    if "annotation_" + entity in lineObject:
                        # documents
                        if lineObject["annotation_" + entity] == 1:
                            countedDocuments[entity] = countedDocuments[entity] + 1
                        # entities
                        if "test_" + entity in lineObject:
                            if "untampered" in lineObject["test_" + entity]:
                                for key in lineObject["test_" + entity]:
                                    for id in lineObject["test_" + entity][key]:
                                        if id not in countedEntities[entity]:
                                            countedEntities[entity].append(id)
                                        if key == "visible":
                                            if id not in visibleEntities[entity]:
                                                visibleEntities[entity].append(id)


    print(dataset)
    print("Documents:")
    for item in countedDocuments:
        print("    " + item + ": " + str(countedDocuments[item]))

    print("Entites:")
    for item in countedEntities:
        print("    " + item + ": " + str(len(countedEntities[item])))

    print("Entites:")
    for item in visibleEntities:
        print("    " + item + ": " + str(len(visibleEntities[item])))
    print()
    print()

if __name__ == "__main__":
    # delete questions
    for dataset in datasets:
        count(dataset)