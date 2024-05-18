import os
import json
import torch
import numpy
import argparse
from PIL import Image
from datasets import Dataset
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration, BitsAndBytesConfig, InstructBlipQFormerModel, InstructBlipQFormerConfig, InstructBlipConfig
from peft import LoraConfig, get_peft_model
import datetime
import math

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
device = "cuda"

entityObjects = [
    {
        "name": "persons",
        "entities": [],
    },
    {
        "name": "locations",
        "entities": [],
    },
    {
        "name": "events",
        "entities": [],
    }
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

def extractNameById(id, entities):
    for entity in entities:
        if id == entity['wd_id']:
            return str(entity['wd_label']).replace("\"", "'").replace("'", "").lower()   

def generateQuestions(size):
    questions = []
    tamperednewsData = []
    print("  - load full base dataset")
    with open('./_datasets/tamperednews/_data/tamperednews_full.jsonl', 'r') as f:
        for line in f:
            tamperednewsData.append(json.loads(line))

    print("  - load entities")
    for entityObject in entityObjects:
        with open(f"./_datasets/tamperednews/entities/{entityObject['name']}.jsonl", 'r') as file:
            for line in file:
                entityObject['entities'].append(json.loads(line))

    print("  - pick random choice")
    rng = numpy.random.default_rng()
    randomSelectionKeys = rng.choice(len(list(tamperednewsData)), size=size, replace=False)
    randomSelectionObjects = [tamperednewsData[i] for i in randomSelectionKeys]

    print("  - prepare questions")
    for lineObject in randomSelectionObjects:
        for entityObject in entityObjects:
            baseQuestion = "\"Is the {} {} visible in this photo ?\""

            # test entites
            for key in lineObject['test_' + entityObject['name']]:
                for entityID in lineObject['test_' + entityObject['name']][key]:
                    question = baseQuestion.format(entityObject['name'][:-1], extractNameById(entityID, entityObject['entities']))
                    if key == 'untampered':
                        questions.append({"id": lineObject['id'], "question": str(question), "answer": "yes"})
                    else:
                        questions.append({"id": lineObject['id'], "question": str(question), "answer": "no"})
    return questions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

class CustomVQADataset(Dataset):
    def __init__(self, img_dir, json_data, processor, transform=None):
        self.img_dir = img_dir
        self.transform = transform
        self.data = json_data
        self.processor = processor

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]['question']
        answer = self.data[idx]['answer']
        image = Image.open(os.path.join(self.img_dir, f"{self.data[idx]['id']}.jpg")).convert("RGB")
        if self.transform:
            image = self.transform(image)

        encoding = self.processor(image, text, padding="max_length", truncation=True, return_tensors="pt").to(device)
        labels = self.processor.tokenizer.encode(answer, return_tensors='pt')
        encoding["labels"] = labels
        
        # remove batch dimension
        for k,v in encoding.items():  
            encoding[k] = v.squeeze()
        return encoding

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def collate_fn(batch):
    processed_batch = {}
    for key in batch[0].keys():
        if key != "text":
            processed_batch[key] = torch.stack([example[key] for example in batch])
        else:
            text_inputs = processor.tokenizer([example["text"] for example in batch], padding=True, return_tensors="pt")
            processed_batch["input_ids"] = text_inputs["input_ids"]
            processed_batch["attention_mask"] = text_inputs["attention_mask"]
    return processed_batch

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    ct = datetime.datetime.now()
    print("current time:-", ct)

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-t5-xl/")
    parser.add_argument("--model-path-tuned", type=str, default="/nfs/home/ernstd/masterthesis_scripts/models/instructblip-flan-finetuned")
    parser.add_argument("--sample-size", type=int, default=1) 
    parser.add_argument("--epochs", type=int, default=1) 
    args = parser.parse_args()

    img_dir = "/nfs/home/ernstd/masterthesis_scripts/_datasets/tamperednews/full_images"

    print("create vlm Instance")
    processor = InstructBlipProcessor.from_pretrained(args.model_path)
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
    )
    config = InstructBlipConfig.from_pretrained(args.model_path)
    model = InstructBlipForConditionalGeneration.from_pretrained(args.model_path).to(device) #, quantization_config=quantization_config)
    for name, param in model.vision_model.named_parameters():
        param.requires_grad = False
        param.grad = None

    for param in model.language_model.parameters():
        param.requires_grad = False
        param.grad = None
    
    print("create dataset")
    trainDatasetData = generateQuestions(args.sample_size)
    validDatasetData = generateQuestions(int(math.ceil(args.sample_size/10)))

    image_transform = transforms.Compose([transforms.Resize([224,224])])
    trainVQADataset = CustomVQADataset(img_dir=img_dir, json_data=trainDatasetData, processor=processor, transform=image_transform)
    validVQADataset = CustomVQADataset(img_dir=img_dir, json_data=validDatasetData, processor=processor, transform=image_transform)

    train_dataloader = DataLoader(trainVQADataset, shuffle=True, batch_size=1, collate_fn=collate_fn)
    valid_dataloader = DataLoader(validVQADataset, shuffle=True, batch_size=1, collate_fn=collate_fn)

    print("prepare training")
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-05)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.9, last_epoch=-1, verbose=True)
    scaler = torch.cuda.amp.GradScaler()

    min_eval_loss = float("inf")
    early_stopping_hook = 0
    patience = 10

    print("start training")
    for epoch in range(args.epochs):
        epoch_loss = 0
        
        # train set
        model.train()
        for batch in train_dataloader:
            pixel_values = batch.pop('pixel_values').to(device, torch.bfloat16)
            labels = batch.pop('labels').to(device)
            input_ids = batch.pop('input_ids').to(device)
            attention_mask = batch.pop('attention_mask').to(device)
            qformer_input_ids = batch.pop('qformer_input_ids').to(device)

            outputs = model(pixel_values=pixel_values, labels=labels, input_ids=input_ids, attention_mask=attention_mask, qformer_input_ids=qformer_input_ids)

            loss = outputs.loss
            epoch_loss += loss.item()
            #loss.backward()
            #optimizer.step()
            optimizer.zero_grad()
            
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

        # valid set
        model.eval() # will notify all layers that you are in eval mode, batchnorm or dropout layers will work in eval mode instead of training mode. 
        with torch.no_grad(): # impacts the autograd engine and deactivate it. It will reduce memory usage and speed up computations but you won’t be able to backprop.
            eval_loss = 0
            for batch in valid_dataloader:
                pixel_values = batch.pop('pixel_values').to(device, torch.bfloat16)
                labels = batch.pop('labels').to(device)
                input_ids = batch.pop('input_ids').to(device)
                attention_mask = batch.pop('attention_mask').to(device)
                qformer_input_ids = batch.pop('qformer_input_ids').to(device)

                outputs = model(pixel_values=pixel_values, labels=labels, input_ids=input_ids, attention_mask=attention_mask, qformer_input_ids=qformer_input_ids)
                    
                loss = outputs.loss
                eval_loss += loss.item()

        print("Epoch: {} - Training loss: {} - Eval Loss: {} - LR: {}".format(epoch+1, epoch_loss/len(train_dataloader), eval_loss/len(valid_dataloader), optimizer.param_groups[0]["lr"]))
        scheduler.step()
        if eval_loss < min_eval_loss:
            model.save_pretrained(f"{args.model_path_tuned}-{args.sample_size}-{args.epochs}", from_pt=True)
            print("Saved model -", datetime.datetime.now())
            min_eval_loss = eval_loss
            early_stopping_hook = 0
        else:
            early_stopping_hook += 1
            if early_stopping_hook > patience:
                break
        torch.cuda.empty_cache()
    print("The finetuning process has done!")
