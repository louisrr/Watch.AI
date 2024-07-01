import pytest
import torch
from unittest.mock import patch, MagicMock
from torch.utils.data import DataLoader
from transformers import RobertaTokenizer, AdamW
from my_script import YourDataset  # Replace with the actual name of your script

@pytest.fixture
def mock_transformers():
    with patch('my_script.RobertaTokenizer') as MockTokenizer, \
         patch('my_script.AdamW') as MockAdamW, \
         patch('my_script.model') as MockModel:
        
        mock_tokenizer = MockTokenizer.from_pretrained.return_value
        mock_adamw = MockAdamW.return_value
        mock_model = MockModel.return_value
        
        yield mock_tokenizer, mock_adamw, mock_model

@pytest.fixture
def example_data():
    texts = ["example sentence", "another example"]
    labels = [0, 1]
    return texts, labels

def test_your_dataset_initialization(mock_transformers, example_data):
    mock_tokenizer, mock_adamw, mock_model = mock_transformers
    texts, labels = example_data
    
    # Create dataset
    dataset = YourDataset(texts, labels)
    
    assert len(dataset) == 2
    assert dataset[0]['input_ids'] is not None
    assert dataset[0]['attention_mask'] is not None
    assert dataset[0]['labels'] == 0

def test_training_loop(mock_transformers, example_data):
    mock_tokenizer, mock_adamw, mock_model = mock_transformers
    texts, labels = example_data
    
    # Mock outputs for model
    mock_outputs = MagicMock()
    mock_outputs.loss = torch.tensor(0.5)
    mock_model.return_value = mock_outputs
    
    # Create dataset and dataloader
    dataset = YourDataset(texts, labels)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mock_model.to.assert_called_with(device)
    
    # Optimizer
    optimizer = AdamW(mock_model.parameters(), lr=1e-5)
    
    # Training loop
    mock_model.train.assert_called()
    for epoch in range(3):  # number of epochs
        for batch in dataloader:
            optimizer.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = mock_model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            print(f"Loss: {loss.item()}")
    
    # Save the model
    mock_model.save_pretrained.assert_called_with('./models')
    mock_tokenizer.save_pretrained.assert_called_with('./models')

