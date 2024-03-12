import json
import csv
import re

models = ['instructBlip_answers', 'blip_2_answers', 'llava_1_5_7b_answers', 'llava_1_5_13b_answers']

#types = ['singleEntity']
#Entity = ['locations']
#category = ['random']
#category_mapping = ['random']
#eric_res = ['0.85']

types = ['singleEntity', 'pairEntity', 'pairLabel']
Entity = ['persons', 'persons', 'persons', 'persons', 'locations', 'locations', 'locations', 'locations', 'events', 'events']
category = ['random', 'country-sensitive', 'gender-sensitive', 'country-gender-sensitive', 'random', 'city-region', 'country-continent', 'region-country', 'random', 'same_instance']
category_mapping = ['random', 'PsC', 'PsG', 'PsCG', 'random', 'LCR', 'LCC', 'LRC', 'random', 'EsP']
eric_res = ['0.95', '0.92', '0.91', '0.92', '0.85', '0.74', '0.84', '0.80', '1.00', '0.74']

for type in types:
    print(type)
    data_TR = []
    for model in models:
        with open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/answers_TR/TR_{type}_{model}.csv", encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_TR.append(row)

    data_PBTR = []
    for model in models:
        with open(f"/nfs/home/ernstd/masterthesis_scripts/document_verification/model_answers/answers_PBTR/PBTR_{type}_{model}.csv", encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_PBTR.append(row)


    for i in range(10):
        selection_TR = []
        selection_PBTR = []

        for answer in data_TR:
            for model in models: 
                if answer['entity'] == Entity[i] and answer['category'] == category[i] and answer['modelname'] == model:
                    selection_TR.append(answer['correct'])
        
        for answer in data_PBTR:
            for model in models: 
                if answer['entity'] == Entity[i] and answer['category'] == category[i] and answer['modelname'] == model:
                    selection_PBTR.append(answer['correct'])

        sentence_0 = "%s & %s & " % (category_mapping[i], eric_res[i])

        sentence_1 = "%s & %s & %s & %s & " % (
            selection_TR[0], selection_TR[1], selection_TR[2], selection_TR[3],
        )

        sentence_2 = "%s & %s & %s & %s \\\\" % (
            selection_PBTR[0], selection_PBTR[1], selection_PBTR[2], selection_PBTR[3]
        )

        numbers_1 = [float(num) for num in re.findall(r'\d+\.\d+', sentence_1)]
        max_number_1 = max(numbers_1)

        numbers_2 = [float(num) for num in re.findall(r'\d+\.\d+', sentence_2)]
        max_number_2 = max(numbers_2)


        sentence_1 = sentence_1.replace(str(max_number_1), r'\textbf{' + str(max_number_1) + r'}')
        sentence_2 = sentence_2.replace(str(max_number_2), r'\textbf{' + str(max_number_2) + r'}')
        print("        " + sentence_0 + sentence_1 + sentence_2)
    print()