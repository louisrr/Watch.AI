import pytest
import torch
from unittest.mock import patch, MagicMock
from data_collection import DynamicDataset, add_data, dataset

@pytest.fixture
def mock_tokenizer():
    with patch('data_collection.RobertaTokenizer') as MockTokenizer:
        mock_instance = MagicMock()
        mock_instance.return_value = {
            'input_ids': [0] * 512,
            'attention_mask': [1] * 512
        }
        MockTokenizer.from_pretrained.return_value = mock_instance
        yield mock_instance

def test_dynamic_dataset_add_sample():
    dataset = DynamicDataset()
    dataset.add_sample("Test text", 1)
    assert len(dataset) == 1
    assert dataset.samples[0] == ("Test text", 1)

def test_dynamic_dataset_len():
    dataset = DynamicDataset()
    dataset.add_sample("Test text 1", 1)
    dataset.add_sample("Test text 2", 0)
    assert len(dataset) == 2

def test_dynamic_dataset_getitem(mock_tokenizer):
    dataset = DynamicDataset()
    dataset.add_sample("Test text", 1)
    item = dataset[0]

    assert 'input_ids' in item
    assert 'attention_mask' in item
    assert 'labels' in item
    assert torch.equal(item['labels'], torch.tensor(1))

def test_add_data():
    # Reset the global dataset before test
    dataset.samples = []
    
    result = add_data("New test text", 0)
    assert result == "Sample added to dataset"
    assert len(dataset) == 1
    assert dataset.samples[0] == ("New test text", 0)
