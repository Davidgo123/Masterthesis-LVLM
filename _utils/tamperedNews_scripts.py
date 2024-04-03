import numpy
import json

subsamples = ['events']

def createSubSample(subsample):
    open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperedNews/_data/tamperedNews_{subsample}.jsonl", 'w').close()

    data = []
    with open('/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperedNews/_data/tamperednews_full.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))

    rng = numpy.random.default_rng()
    randomSelectionKeys = rng.choice(len(list(data)), size=1000, replace=False)

    with open(f"/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperedNews/_data/tamperedNews_{subsample}.jsonl", 'a') as f:
        for key in randomSelectionKeys:
            if len(data[key]['text_' + subsample]) > 0:
                f.write(json.dumps(data[key]) + "\n")

def countData():

    data = {
        "person": 0,
        "location": 0,
        "event": 0
    }

    ids = []
    
    with open('/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperedNews/tamperednews.jsonl', 'r') as f:
        for line in f:
            counter = 0
            line = json.loads(line)
            
            if line['annotation_persons'] == 1:
                counter += 1
                data["person"] += 1
            if line['annotation_locations'] == 1:
                counter += 1
                data["location"] += 1
            if line['annotation_events'] == 1:
                counter += 1
                data["event"] += 1

            # ids with more than one visible categories
            if counter > 1:
                ids.append(line['id'])
                
        print(data)
        print(ids)


if __name__ == "__main__":
    countData()
    # delete questions
    #for subsample in subsamples:
    #    createSubSample(subsample)