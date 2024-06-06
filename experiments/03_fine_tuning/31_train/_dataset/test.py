import json

if __name__ == "__main__":

    with open(f"./experiments/03_fine_tuning/310_train/_dataset/dataset_test.json", 'r') as file:
        object = json.load(file)
        
        max = 0
        for counter, item in enumerate(object):
            #
            if (len(str(item)) > 1000):
                if len(str(item)) > max:
                    max = len(str(item))
                print(f"counter: {counter} = len: {len(str(item))}")
                print()

        print(max)