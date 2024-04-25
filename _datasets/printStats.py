import json

datasets = [
    "news400/news400_merged.jsonl",
    "tamperednews/tamperednews.jsonl"
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

    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/{dataset}", 'r') as f:
        for line in f:
            lineObject = json.loads(line)

            entities = ["persons", "locations", "events"]
            for entity in entities:
                if "annotation_" + entity in lineObject:
                    # documents
                    if lineObject["annotation_" + entity]:
                        countedDocuments[entity] = countedDocuments[entity] + 1
                    # entities
                    if "test_" + entity in lineObject:
                        if "untampered" in lineObject["test_" + entity]:
                            for key in lineObject["test_" + entity]:
                                for id in lineObject["test_" + entity][key]:
                                    if id not in countedEntities[entity]:
                                        countedEntities[entity].append(id)
    print(dataset)
    print("Documents:")
    for item in countedDocuments:
        print("    " + item + ": " + str(countedDocuments[item]))

    print("Entites:")
    for item in countedEntities:
        print("    " + item + ": " + str(len(countedEntities[item])))
    print()
    print()

if __name__ == "__main__":
    # delete questions
    for dataset in datasets:
        count(dataset)