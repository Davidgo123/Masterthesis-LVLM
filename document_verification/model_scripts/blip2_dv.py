import requests
import argparse
from PIL import Image
import os
import json
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from transformers import AutoProcessor, AutoModelForVisualQuestionAnswering, AutoTokenizer

def run_model(args):
    device = "cuda"
    answerFile = f"{args.answer_file_path}blip_2_answers_{args.iteration}.jsonl"
    open(answerFile, "w").close()

    processor = AutoProcessor.from_pretrained(args.model_path, local_files_only=True)
    model = AutoModelForVisualQuestionAnswering.from_pretrained(args.model_path, local_files_only=True, torch_dtype=torch.float16).to(device)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)

            # load content
            image = Image.open(f"{args.image_folder}/{question['image']}")
            prompt = f"Question: {question['text']} Answer:"

            inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch.float16)

            outputs = model.generate(**inputs)
            generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

            with open(answerFile, "a") as outfile:
                outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"text\": \"%s\", \"truth_label\": \"%s\", \"wrong_label\": \"%s\", \"entity\": \"%s\", \"category\": \"%s\"}\n""" % (str(question['question_id']), str(question['image']), str(question['text']), str(generated_text), str(question['truth_label']), str(question['wrong_label']), str(question['entity']), str(question['category'])))

def run_model_single_entity(args):
    device = "cuda"
    answerFile = f"{args.answer_file_path}blip_2_answers_{args.iteration}.jsonl"
    open(answerFile, "w").close()

    processor = AutoProcessor.from_pretrained(args.model_path, local_files_only=True)
    model = AutoModelForVisualQuestionAnswering.from_pretrained(args.model_path, local_files_only=True, torch_dtype=torch.float16).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, local_files_only=True)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)

            # load content
            image = Image.open(f"{args.image_folder}/{question['image']}")
            prompt = f"Question: {question['text']} Answer:"
            inputs = processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)

            # ---------------

            output = model.generate(**inputs)
            answer = processor.batch_decode(output, skip_special_tokens=True)[0].strip()

            # ---------------

            # Scores für beide Antworten (Ja und Nein) erhalten

            output = model(**inputs)
            logits = output.logits
            scores = nn.functional.softmax(logits, dim=-1)
            max_probabilities, max_indices = torch.max(scores, dim=1)

            scoreA = max_probabilities[0][processor.tokenizer.convert_tokens_to_ids("A")] * 100
            scoreB = max_probabilities[0][processor.tokenizer.convert_tokens_to_ids("B")] * 100

            # Scores für Ja und Nein ausgeben
            print(f"ID: {question['question_id']}")
            print("Score für 'a'  :", scoreA)
            print("Score für 'b'  :", scoreB)

            # Ausgeben der Antwort
            print("Antwort:", answer)
            print()

            # ---------------

           # with open(answerFile, "a") as outfile:
           #     outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"text\": \"%s\", \"entity\": \"%s\", \"category\": \"%s\"}\n""" % (str(question['question_id']), str(question['image']), str(question['text']), str(generated_text), str(question['entity']), str(question['category'])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/blip2-opt-2.7b/")
    parser.add_argument("--image-folder", type=str, default="/nfs/home/ernstd/data/news400/images")
    parser.add_argument("--question-file", type=str, default="")
    parser.add_argument("--answer-file-path", type=str, default="")
    parser.add_argument("--iteration", type=int, default=0)
    args = parser.parse_args()

    run_model_single_entity(args)
