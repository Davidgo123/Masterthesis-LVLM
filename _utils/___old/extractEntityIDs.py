import json

datasets = {
    "news400": {
        "path": "news400/news400_merged.jsonl",
        "ids": {
            "persons": [],
            "locations": [],
            "events": []
        }
    },
    "tamperedNews": {
        "path": "tamperedNews/tamperednews.jsonl",
        "ids": {
            "persons": [],
            "locations": [],
            "events": []
        }
    }
}

for dataset in datasets:
    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/{datasets[dataset]["path"]}", 'r') as file:

        for line in file:
            data = json.loads(line)

            if data["annotation_persons"] == 1:
                for category in data['test_persons']:
                    for id in data['test_persons'][category]:
                        if id not in datasets[dataset]["ids"]['persons']:
                            datasets[dataset]["ids"]['persons'].append(id)
                        
            if data["annotation_locations"] == 1:
                for category in data['test_locations']:
                    for id in data['test_locations'][category]:
                        if id not in datasets[dataset]["ids"]['locations']:
                            datasets[dataset]["ids"]['locations'].append(id)

            if data["annotation_events"] == 1:
                for category in data['test_events']:
                    for id in data['test_events'][category]:
                        if id not in datasets[dataset]["ids"]['events']:
                            datasets[dataset]["ids"]['events'].append(id)


with open("/nfs/home/ernstd/masterthesis_scripts/_datasets/entityIDs.json", "w") as file:
    json.dump(datasets, file)