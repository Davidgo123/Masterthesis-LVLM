import json

locations= []
events= []

types_locations = ["untampered", "random", "country-continent", "region-country", "city-region", "visible"]
types_events = ["untampered", "random", "same_instance", "visible"]

#types_locations = ["visible"]
#types_events = ["visible"]

def countNews400():
    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/news400/news400_merged.jsonl", 'r') as f:
        for line in f:
            lineObject = json.loads(line)

            # locations
            for type in types_events:
                if type in lineObject['test_locations']:
                    for test_location in lineObject['test_locations'][type]:
                        if test_location not in locations:
                            locations.append(test_location)

            # events
            for type in types_events:
                if type in lineObject['test_events']:
                    for test_location in lineObject['test_events'][type]:
                        if test_location not in events:
                            events.append(test_location)

    print(locations)
    print(events)
    print("- - - - - - - - - -")
    print(len(locations))
    print(len(events))
    print("- - - - - - - - - -")

if __name__ == "__main__":
    # delete questions
    countNews400()