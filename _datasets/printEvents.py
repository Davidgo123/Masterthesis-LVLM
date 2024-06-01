import json
import pprint

datasets = [
    "news400/news400_merged.jsonl",
    "tamperednews/tamperednews.jsonl",
]

def count(dataset):
    
    events = {
        "all": [],
        "visible": []
    }

    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/{dataset}", 'r') as f:
        for line in f:
            lineObject = json.loads(line)

            if lineObject["annotation_events"] == 1:
                for event in lineObject["text_events"]:
                    object = {
                        "wd_id": event["wd_id"],
                        "text": event["text"],
                        "wd_label": event["wd_label"]
                    }
                    if object not in events['all']:
                        events['all'].append(object)
                
                if "untampered" in lineObject["test_events"]:
                    for event in lineObject["test_events"]["untampered"]: 
                        obs = [obj for obj in events["all"] if(obj['wd_id'] == event)][0]
                        if obs not in events["visible"]:
                            events["visible"].append(obs['wd_label'])

    pprint.pprint(events["visible"])
    print()
    print()
    print()
    print()

if __name__ == "__main__":
    # delete questions
    for dataset in datasets:
        count(dataset)