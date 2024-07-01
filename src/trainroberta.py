import torch
from torch.utils.data import DataLoader
from transformers import RobertaTokenizer, AdamW

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Example dataset
class YourDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Example data
texts = ["example sentence", "another example"]
labels = [0, 1]  # Example labels

# Create dataset and dataloader
dataset = YourDataset(texts, labels)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# Setup GPU or CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

# Training loop
model.train()
for epoch in range(3):  # number of epochs
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(f"Loss: {loss.item()}")

# Save the model
model.save_pretrained('./models')
tokenizer.save_pretrained('./models')
