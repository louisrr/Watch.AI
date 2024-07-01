# data_collection.py
from transformers import RobertaTokenizer
from torch.utils.data import Dataset

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

class DynamicDataset(Dataset):
    def __init__(self):
        self.samples = []

    def add_sample(self, text, label):
        self.samples.append((text, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        text, label = self.samples[idx]
        encoding = tokenizer(text, truncation=True, padding='max_length', max_length=512)
        return {**encoding, 'labels': torch.tensor(label)}

# Create a global dataset instance that can be accessed by other modules
dataset = DynamicDataset()

def add_data(text, label):
    dataset.add_sample(text, label)
    return "Sample added to dataset"
