import requests
import argparse
from PIL import Image
import os
import json
import torch
from transformers import AutoProcessor, AutoModelForPreTraining, BitsAndBytesConfig

def run_model(args):
    open(args.answer_file, 'w').close()

    processor = AutoProcessor.from_pretrained(args.model_path, local_files_only=True)
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    model = AutoModelForPreTraining.from_pretrained(args.model_path, local_files_only=True, quantization_config=quantization_config)

    with open(args.question_file, 'r') as file:
        for line in file:
            question = json.loads(line)

            # load content
            image = Image.open(f"{args.image_folder}/{question['image']}")
            prompt = f"USER: <image>{question['text']} ASSISTANT:"

            inputs = processor(text=prompt, images=image, return_tensors="pt").to('cuda')
            output = model.generate(**inputs, do_sample=False, max_new_tokens=20)
            generated_text = processor.batch_decode(output, skip_special_tokens=True)[0].strip()
            answer = generated_text[str(generated_text).find("ASSISTANT: ") + len("ASSISTANT: "):]

            with open(args.answer_file, "a") as outfile:
                outfile.write("""{\"question_id\": \"%s\", \"image\": \"%s\", \"question\": \"%s\", \"text\": \"%s\", \"truth_label\": \"%s\", \"test_entity\": \"%s\", \"test_label\": \"%s\"}\n""" % (str(question['question_id']), str(question['image']), str(question['text']), str(answer), str(question['truth_label']), str(question['test_entity']), str(question['test_label'])))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/llava-1.5-13b-hf/")
    parser.add_argument("--image-folder", type=str, default="/nfs/home/ernstd/data/news400/images")
    parser.add_argument("--question-file", type=str, default="/nfs/home/ernstd/data/news400/document_verification/questions.jsonl")
    parser.add_argument("--answer-file", type=str, default="/nfs/home/ernstd/data/news400/document_verification/llava_1_5_13_answers.jsonl")
    args = parser.parse_args()

    run_model(args)
