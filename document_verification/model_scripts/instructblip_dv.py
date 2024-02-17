import argparse
from PIL import Image
import json
import torch
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
from torch import nn


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


answerFullSet = {
    "A": {
        'index': 0,
        'token': ['A']
    },
    "B": {
        'index': 1,
        'token': ['B']
    },
    "yes": {
        'index': 0,
        'token': ['Yes']
    },
    "no": {
        'index': 1,
        'token': ['No']
    },
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


class instructBlipInstance:
    def __init__(self, args):
        self.processor = InstructBlipProcessor.from_pretrained(args.model_path)
        self.model = InstructBlipForConditionalGeneration.from_pretrained(args.model_path, torch_dtype=torch.float16)
        self.model.to(args.device)


    # clean up answer file
    def cleanAnswers(self, answerFile):
        open(answerFile, "w").close()
        

    # return answer of model
    def getResponse(self, args, prompt, image):
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.bfloat16)
        with torch.no_grad():
            outputs = self.model.generate(**inputs)
        return self.processor.batch_decode(outputs, skip_special_tokens=True)


    # set token ids for token probability
    def setTokenIDs(self, label1, label2):
        self.index2label = {}
        self.answer_sets = {}
        self.answer_sets_token_id = {}

        self.index2label[answerFullSet[label1]['index']] = label1
        self.index2label[answerFullSet[label2]['index']] = label2
        self.answer_sets[label1] = answerFullSet[label1]['token']
        self.answer_sets[label2] = answerFullSet[label2]['token']
    
        self.index2label = dict(sorted(self.index2label.items()))
        self.answer_sets = dict(sorted(self.answer_sets.items()))

        for label, answer_set in self.answer_sets.items():
            self.answer_sets_token_id[label] = []
            for answer in answer_set:
                self.answer_sets_token_id[label].append(self.processor.tokenizer.convert_tokens_to_ids(answer))
        

    # return probability
    def getResponsePBC(self, args, prompt, image):   
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(args.device, torch.float16)
        with torch.no_grad(): 
            outputs = self.model.generate(**inputs, output_scores=True, return_dict_in_generate=True)
            print(nn.functional.softmax(outputs.scores[0][:, [29874, 29909, 29890, 29933]], dim=-1))
        pbc_probas = outputs.scores[0][:, self.answer_sets_token_id[self.index2label.get(0)] + self.answer_sets_token_id[self.index2label.get(1)]].softmax(-1)
        yes_proba_matrix = pbc_probas[:, :len(self.answer_sets.get(self.index2label.get(0)))].sum(dim=1)
        no_proba_matrix = pbc_probas[:, len(self.answer_sets.get(self.index2label.get(0))):].sum(dim=1)
        probas = torch.cat((yes_proba_matrix.reshape(-1, 1), no_proba_matrix.reshape(-1, 1)), -1)

        max_probas_token = torch.max(probas, dim=1)
        sequence_probas = [float(proba) for proba in max_probas_token.values]
        sequences = [self.index2label.get(int(indice)) for indice in max_probas_token.indices]
        return sequences, sequence_probas
    

    # save answer from model
    def saveAnswer(self, answerFile, question, modelResponse, probability):
        with open(answerFile, "a") as outfile:
            outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"text\": \"%s\", \"probability\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\", \"entity\": \"%s\", \"category\": \"%s\"}\n""" % (str(question['question_id']), str(question['image']), str(question['text']), str(modelResponse), str(probability), str(question['truth_label']), str(question['wrong_label']), str(question['entity']), str(question['category'])))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# run model
def run(args, answerFile):
    instructBlip = instructBlipInstance(args)
    instructBlip.cleanAnswers(answerFile)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)
            prompt = f"Question: {question['text']} Answer:"
            instructBlip.setTokenIDs(question['truth_label'], question['wrong_label'])
            modelResponse = instructBlip.getResponse(args, prompt, Image.open(f"{args.image_folder}/{question['image']}"))
            modelResponsePBC = instructBlip.getResponsePBC(args, prompt, Image.open(f"{args.image_folder}/{question['image']}"))
            #instructBlip.saveAnswer(answerFile, question, modelResponse, round(modelResponsePBC[1][0], 2))

            print("Reponse: " + str(modelResponse))
            print(modelResponsePBC)
            print(round(modelResponsePBC[1][0], 2))
            print()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/instructblip-vicuna-7b/")
    parser.add_argument("--image-folder", type=str, default="/nfs/home/ernstd/data/news400/images")
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--answer-file-path", type=str, default="")
    parser.add_argument("--answer-file-name", type=str, default="")
    parser.add_argument("--iteration", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    answerFile = f"{args.answer_file_path}{args.answer_file_name}_{args.iteration}.jsonl"
    run(args, answerFile)

