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
        with open(f'/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperedNews/images.json','r') as ids:
            imageIDS = json.load(ids)
            for key in randomSelectionKeys:
                if len(data[key]['text_' + subsample]) > 0:
                    if data[key]['id'] in imageIDS:
                        f.write(json.dumps(data[key]) + "\n")

if __name__ == "__main__":
    # delete questions
    for subsample in subsamples:
        createSubSample(subsample)