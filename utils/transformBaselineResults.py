import glob
import json

# - - - - - - - - - - - - - - - - - - - - - - - - - - - 

cnnData = []

files = [
    {
        "output": "./output/model_answers/11_DV-news400-baseline.jsonl",
        "input": "./experiments/01_without_comparative_images/11_document_verification/_questions/questions_news400.jsonl"
    },
    {
        "output": "./output/model_answers/11_DV-tamperednews-baseline.jsonl",
        "input": "./experiments/01_without_comparative_images/11_document_verification/_questions/questions_tamperednews.jsonl"
    },
    {
        "output": "./output/model_answers/12_EV-news400-baseline.jsonl",
        "input": "./experiments/01_without_comparative_images/12_entity_verification/_questions/questions_news400.jsonl"
    },
    {
        "output": "./output/model_answers/12_EV-tamperednews-baseline.jsonl",
        "input": "./experiments/01_without_comparative_images/12_entity_verification/_questions/questions_tamperednews.jsonl"
    }   
]

for file in files:
    open(file["output"], 'w').close()
    dataset = file["output"].split("/")[-1].split("-")[1]
    for filenames in glob.glob(f"./output/cnn-baseline/*{dataset}*_similarities.jsonl"):
        with open(f"{filenames}", mode='r', encoding="utf-8") as cnnFile:
            for line in cnnFile:
                cnnData.append(json.loads(line))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def filterfunc(question):
    for x in cnnData:
        if question["question_id"] == x["document_id"]:
            for entityType in x["entity_similarities"]:
                for id in x["entity_similarities"][entityType]:
                    if str(id) == str(question["entityID"]):
                        prob = round(x["entity_similarities"][entityType][id], 2)

                        if prob < 0.5:
                            return prob, "no", "no"
                        else:
                            return prob, "yes", "yes"
                            
    return " - ", " - ", " - "


for file in files:
    with open(f"{file["input"]}", mode='r', encoding="utf-8") as questionFile:
        with open(file["output"], "a") as outputFile:
            for line in questionFile:
                question = json.loads(line)


                prob, response, probText = filterfunc(question)              

                outputFile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"entityID\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\", \"response\": \"%s\", \"probText\": \"%s\", \"prob\": \"%s\"}\n""" 
                % (str(question['question_id']), str(question['image']), str(question['question']), str(question['entity']), str(question['testlabel']), str(question['set']), str(question['entityID']), str(question['gTruth']), str(question['gWrong']), str(response), str(probText), str(prob)))







