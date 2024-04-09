import argparse
from PIL import Image
import json
import torch
import random
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


answerFullSet = {
    "A": {
        'index': 0,
        'token': ['A', 'a']
    },
    "B": {
        'index': 1,
        'token': ['B', 'b']
    },
    "yes": {
        'index': 0,
        'token': ['Yes', 'yes']
    },
    "no": {
        'index': 1,
        'token': ['No', 'no']
    },
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


class instructBlipInstance:
    def __init__(self, args):
        self.processor = InstructBlipProcessor.from_pretrained(args.model_path)
        self.model = InstructBlipForConditionalGeneration.from_pretrained(args.model_path, torch_dtype=torch.float16)
        self.model.to(args.device)

    # - - - - - - - - - - - - - - - -

    # clean up answer file
    def cleanAnswers(self, answerFile):
        open(answerFile, "w").close()
        
    # set token ids for token probability
    def setTokenIDs(self, label1, label2):
        self.index2label = {
            answerFullSet[label1]['index']: label1,
            answerFullSet[label2]['index']: label2
        }
        self.answer_sets = {
            label1: answerFullSet[label1]['token'],
            label2: answerFullSet[label2]['token']
        }

        self.index2label = dict(sorted(self.index2label.items()))
        self.answer_sets = dict(sorted(self.answer_sets.items()))

        self.answer_sets_token_id = {}
        for label, answer_set in self.answer_sets.items():
            self.answer_sets_token_id[label] = []
            for answer in answer_set:
                self.answer_sets_token_id[label] += self.processor.tokenizer.encode(answer, add_special_tokens=False)

    # - - - - - - - - - - - - - - - -

    # return answer of model
    def getResponse(self, args, prompt, image):
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.float16)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=1)
        return self.processor.batch_decode(outputs, skip_special_tokens=True)[0]

    # return probability
    def getProbabilities(self, args, prompt, image):   
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.float16)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=1, output_scores=True, return_dict_in_generate=True)
            
        probas = outputs.scores[0][:, self.answer_sets_token_id[self.index2label.get(0)] + self.answer_sets_token_id[self.index2label.get(1)]].softmax(-1)
        label1_proba_matrix = probas[:, :len(self.answer_sets[self.index2label.get(0)])].sum(dim=1)
        label2_proba_matrix = probas[:, len(self.answer_sets[self.index2label.get(0)]):].sum(dim=1)
        label_probas = torch.cat((label1_proba_matrix.reshape(-1, 1), label2_proba_matrix.reshape(-1, 1)), -1)
        max_probas_token = torch.max(label_probas, dim=1)
        
        sequence_probas = [float(proba) for proba in max_probas_token.values]
        sequence = [self.index2label.get(int(indice)) for indice in max_probas_token.indices]
        return sequence[0], round(sequence_probas[0], 2)
    
    # - - - - - - - - - - - - - - - -

    # save answer from model
    def saveAnswer(self, answerFile, question, response, probText, prob):
        with open(answerFile, encoding="utf-8", mode="a") as outfile:
            outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"entity\": \"%s\", \"testlabel\": \"%s\", \"set\": \"%s\", \"gTruth\": \"%s\", \"gWrong\": \"%s\", \"response\": \"%s\", \"probText\": \"%s\", \"prob\": \"%s\"}\n""" 
                % (str(question['question_id']), str(question['image']), str(question['question']), str(question['entity']), str(question['testlabel']), str(question['set']), str(question['gTruth']), str(question['gWrong']), str(response), str(probText), str(prob)))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# run model
def run(args, answerFile):
    instBlip = instructBlipInstance(args)
    instBlip.cleanAnswers(answerFile)

    questions = []
    with open(args.question_file, encoding="utf-8", mode='r') as file:
        for line in file:
            questions.append(json.loads(line))

        random.shuffle(questions)
        for question in questions:
            prompt = f"Question: {question['question']} Answer:"
            instBlip.setTokenIDs(question["gTruth"], question["gWrong"])
            response = instBlip.getResponse(args, prompt, Image.open(f"{question['image']}"))
            probText, prob = instBlip.getProbabilities(args, prompt, Image.open(f"{question['image']}"))
            instBlip.saveAnswer(answerFile, question, response, probText, prob)  

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/instructblip-vicuna-7b/")
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--answer-file-path", type=str, default="")
    parser.add_argument("--answer-file-name", type=str, default="")
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    answerFile = f"{args.answer_file_path}{args.answer_file_name}.jsonl"
    run(args, answerFile)

