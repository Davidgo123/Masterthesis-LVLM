import numpy
import json

subsamples = ['events']

def createSubSample(subsample):
    open(f"./_datasets/tamperednews/_data/tamperednews_{subsample}.jsonl", 'w').close()

    data = []
    with open('./_datasets/tamperednews/_data/tamperednews_full.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))

    rng = numpy.random.default_rng()
    randomSelectionKeys = rng.choice(len(list(data)), size=1000, replace=False)

    with open(f"./_datasets/tamperednews/_data/tamperednews_{subsample}.jsonl", 'a') as f:
        for key in randomSelectionKeys:
            if len(data[key]['text_' + subsample]) > 0:
                f.write(json.dumps(data[key]) + "\n")
                

if __name__ == "__main__":
    # delete questions
    for subsample in subsamples:
        createSubSample(subsample)