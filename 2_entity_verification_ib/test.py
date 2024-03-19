import argparse
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForPreTraining


class instructBlipInstance:
    def __init__(self, args):
        self.processor = AutoProcessor.from_pretrained(args.model_path)
        self.model = AutoModelForPreTraining.from_pretrained(args.model_path, torch_dtype=torch.float16)
        self.model.to(args.device)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# run model
def run(args, blip, question, image):
    prompt = f"<image> USER:{question} ASSISTANT:"
    inputs = blip.processor(images=Image.open(f"{image}"), text=prompt, return_tensors="pt").to(args.device, torch.float16)
    outputs = blip.model.generate(**inputs, max_new_tokens=256)
    TR = blip.processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    text = TR[str(TR).find("ASSISTANT: ") + len("ASSISTANT: "):]
    print("Answer:" + text.replace("\n", ""))
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/models/llava-v1.6-mistral-7b-hf/")
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()
    
    blip = instructBlipInstance(args)
    
    images = {
        "/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_4_bo.jpg": {
            #"What do you see in the part with the red border?",
            #"What do you see in the part with the blue border?",
            "Does the red part of the image show the same person as the blue part of the image?"
        },
        "/nfs/home/ernstd/masterthesis_scripts/2_entity_verification_ib/images/template_4_p.jpg": {
            #"What do you see in the part with the red border?",
            #"What do you see in the part with the blue border?",
            "Does the red part of the image show the same location (city) as the blue part of the image?"
        }
    }

    for image in images:
        for question in images[image]:
            run(args, blip, question, image)
            print()
            print()
