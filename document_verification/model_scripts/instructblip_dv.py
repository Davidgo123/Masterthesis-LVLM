import requests
import argparse
from PIL import Image
import os
import json
import torch
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration, BitsAndBytesConfig

def run_model(args):
    device = "cuda"
    open(args.answer_file, 'w').close()
    
    processor = InstructBlipProcessor.from_pretrained(args.model_path, local_files_only=True)
    model = InstructBlipForConditionalGeneration.from_pretrained(args.model_path, local_files_only=True, torch_dtype=torch.float16).to(device)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)

            # load content
            image = Image.open(f"{args.image_folder}/{question['image']}")
            prompt = f"{question['text']}"

            inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch.float16)

            outputs = model.generate(**inputs, do_sample=False, max_new_tokens=20)
            generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

            with open(args.answer_file, "a") as outfile:
                outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"text\": \"%s\", \"truth_label\": \"%s\", \"test_entity\": \"%s\", \"test_label\": \"%s\"}\n""" % (str(question['question_id']), str(question['image']), str(question['text']), str(generated_text), str(question['truth_label']), str(question['test_entity']), str(question['test_label'])))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/instructblip-vicuna-7b/")
    parser.add_argument("--image-folder", type=str, default="/nfs/home/ernstd/data/news400/images")
    parser.add_argument("--question-file", type=str, default="/nfs/home/ernstd/data/news400/document_verification/questions.jsonl")
    parser.add_argument("--answer-file", type=str, default="/nfs/home/ernstd/data/news400/document_verification/instructblip_answers.jsonl")
    args = parser.parse_args()

    run_model(args)
