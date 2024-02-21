import argparse
from PIL import Image
import json
import torch
from transformers import AutoProcessor, Blip2ForConditionalGeneration
from torch import nn


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


answerFullSet = {
    "A": {
        'index': 0,
        'token': [' A', ' a']
    },
    "B": {
        'index': 1,
        'token': [' B', ' b']
    },
    "yes": {
        'index': 0,
        'token': [' Yes', ' yes']
    },
    "no": {
        'index': 1,
        'token': [' No', ' no']
    },
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


class blipInstance:
    def __init__(self, args):
        self.processor = AutoProcessor.from_pretrained(args.model_path)
        self.model = Blip2ForConditionalGeneration.from_pretrained(args.model_path, torch_dtype=torch.float16)
        self.model.to(args.device)


    # clean up answer file
    def cleanAnswers(self, answerFile):
        open(answerFile, "w").close()
        

    # return answer of model
    def getResponse(self, args, prompt, image):
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.float16)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=1)
        return self.processor.batch_decode(outputs, skip_special_tokens=True)[0]


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

    # return probability
    def getResponsePBC(self, args, prompt, image):   
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.float16)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=1, output_scores=True, return_dict_in_generate=True)
            
        pbc_probas = outputs.scores[0][:, self.answer_sets_token_id[self.index2label.get(0)] + self.answer_sets_token_id[self.index2label.get(1)]].softmax(-1)
        yes_proba_matrix = pbc_probas[:, :len(self.answer_sets[self.index2label.get(0)])].sum(dim=1)
        no_proba_matrix = pbc_probas[:, len(self.answer_sets[self.index2label.get(0)]):].sum(dim=1)
        probas = torch.cat((yes_proba_matrix.reshape(-1, 1), no_proba_matrix.reshape(-1, 1)), -1)

        max_probas_token = torch.max(probas, dim=1)
        sequence_probas = [float(proba) for proba in max_probas_token.values]
        sequences = [self.index2label.get(int(indice)) for indice in max_probas_token.indices]
        return sequences, sequence_probas
    

    # save answer from model
    def saveAnswer(self, answerFile, question, TR, PBTR, PB):
        with open(answerFile, "a") as outfile:
            outfile.write("""{\"question_id\": \"%s_%s_%s\", \"questionType\": \"%s\", \"image\": \"%s\", \"entity\": \"%s\", \"category\": \"%s\", \"question\": \"%s\", \"TR\": \"%s\", \"PBTR\": \"%s\", \"PB\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\"}\n""" % (str(question['question_id']), str(question['entity']), str(question['category']), str(question['questionType']), str(question['image']), str(question['entity']), str(question['category']), str(question['text']), str(TR), str(PBTR), str(PB), str(question['truth_label']), str(question['wrong_label'])))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# run model
def run(args, answerFile):
    blip = blipInstance(args)
    blip.cleanAnswers(answerFile)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)
            prompt = f"Question: {question['text']} Answer:"
            blip.setTokenIDs(question["truth_label"], question["wrong_label"])            
            TR = blip.getResponse(args, prompt, Image.open(f"{args.image_folder}/{question['image']}")).replace("\n", "")
            PBTR, PB = blip.getResponsePBC(args, prompt, Image.open(f"{args.image_folder}/{question['image']}"))
            blip.saveAnswer(answerFile, question, TR, PBTR[0], round(PB[0], 2))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/blip2-opt-2.7b/")
    parser.add_argument("--image-folder", type=str, default="/nfs/home/ernstd/data/news400/images")
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--answer-file-path", type=str, default="")
    parser.add_argument("--answer-file-name", type=str, default="")
    parser.add_argument("--iteration", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    answerFile = f"{args.answer_file_path}{args.answer_file_name}_{args.iteration}.jsonl"
    run(args, answerFile)