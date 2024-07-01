from fastapi import FastAPI, WebSocket
import json
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from torch import nn
import asyncio

app = FastAPI()


# Assuming you have a function to load your model and tokenizer
def load_model_and_tokenizer():
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = RobertaForSequenceClassification.from_pretrained('roberta-base')
    return model, tokenizer

model, tokenizer = load_model_and_tokenizer()

# Load excluded topics
with open('excluded_topics.json', 'r') as file:
    excluded_topics = json.load(file)

@app.websocket("/input") # this is the endpoint we hit to send the actual text prompt for the LLM to generate videos and photos
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = await check_text(data)
        await websocket.send_text(json.dumps(result))

# Define the function to check text against excluded topics
async def check_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    probs = nn.functional.softmax(outputs.logits, dim=-1)
    topic_id = probs.argmax().item()  # Assuming you have mapped topics to IDs in your model

    # Map the model's output to your excluded topics
    for topic, id in excluded_topics.items():
        if id == topic_id:
            return {'text': text, 'excluded': True, 'topic': topic}
    
    return {'text': text, 'excluded': False}

# import pytorch
# import opencv
# import matplotlib
# import pandas
# import keras
# from fastapi import FastAPI, HTTPexception

# LLM function to process text  input
	# We may consider forking this code here: https://github.com/LargeWorldModel/LWM

# LLM security service - DONE
	# We can use RoBERTa as a security AI to catch certain things from being injected into the code
	# https://github.com/facebookresearch/fairseq/tree/main/examples/roberta

# Child abuse prevention system - DONE
	# We could potentially use RoBERTa for this as well
	# https://github.com/facebookresearch/fairseq/tree/main/examples/roberta

# argon2 session hash
