import json

open('/nfs/home/ernstd/data/news400/news400_merged.jsonl', 'w').close()

validatedData = []
with open('/nfs/home/ernstd/data/news400/_data/news400_validated.jsonl', 'r') as validatedFile:
    for line in validatedFile:
        lineObject = json.loads(line)
        validatedData.append(lineObject)

with open('/nfs/home/ernstd/data/news400/news400_merged.jsonl', 'a') as mergedFile:
    with open('/nfs/home/ernstd/data/news400/_data/news400.jsonl', 'r') as orginal:
        for line in orginal:
            orgLineObject = json.loads(line)
                
            for item in validatedData:
                if orgLineObject['id'] == item['id']:
                    if 'untampered' in item['test_persons']:
                        if len(orgLineObject['test_persons']['untampered']) > 0:
                            orgLineObject['test_persons']['visible'] = item['test_persons']['untampered']

                    if 'untampered' in item['test_locations']:
                        if len(orgLineObject['test_locations']['untampered']) > 0:
                            orgLineObject['test_locations']['visible'] = item['test_locations']['untampered']

                    if 'untampered' in item['test_events']:
                        if len(orgLineObject['test_events']['untampered']) > 0:
                            orgLineObject['test_events']['visible'] = item['test_events']['untampered']

                    orgLineObject['annotation_persons'] = item['annotation_persons']
                    orgLineObject['annotation_locations'] = item['annotation_locations']
                    orgLineObject['annotation_events'] = item['annotation_events']

                    mergedFile.write(json.dumps(orgLineObject) + "\n")
                    break