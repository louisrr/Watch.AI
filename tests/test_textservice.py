import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import WebSocket
from my_fastapi_app import app, load_model_and_tokenizer, check_text  # Replace with the actual name of your FastAPI app script
import asyncio

client = TestClient(app)

@pytest.fixture
def mock_transformers():
    with patch('my_fastapi_app.RobertaTokenizer') as MockTokenizer, \
         patch('my_fastapi_app.RobertaForSequenceClassification') as MockModel:
        
        mock_tokenizer = MockTokenizer.from_pretrained.return_value
        mock_model = MockModel.from_pretrained.return_value
        
        yield mock_tokenizer, mock_model

@pytest.fixture
def mock_excluded_topics():
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
            "example_topic": 0
        })
        yield mock_open

@pytest.fixture
def mock_check_text():
    with patch('my_fastapi_app.check_text') as mock_check:
        yield mock_check

@pytest.mark.asyncio
async def test_websocket_endpoint(mock_transformers, mock_excluded_topics, mock_check_text):
    mock_tokenizer, mock_model = mock_transformers
    
    mock_check_text.return_value = {
        'text': "Test input",
        'excluded': True,
        'topic': "example_topic"
    }
    
    async with client.websocket_connect("/input") as websocket:
        await websocket.send_text("Test input")
        response = await websocket.receive_text()
        result = json.loads(response)
        
        assert result == {
            'text': "Test input",
            'excluded': True,
            'topic': "example_topic"
        }
        mock_check_text.assert_called_once_with("Test input")

# Additional tests for individual functions

def test_load_model_and_tokenizer(mock_transformers):
    model, tokenizer = load_model_and_tokenizer()
    assert model is not None
    assert tokenizer is not None
    mock_transformers[0].from_pretrained.assert_called_once_with('roberta-base')
    mock_transformers[1].from_pretrained.assert_called_once_with('roberta-base')

@pytest.mark.asyncio
async def test_check_text(mock_transformers, mock_excluded_topics):
    mock_tokenizer, mock_model = mock_transformers
    mock_tokenizer.return_value = {"input_ids": [0], "attention_mask": [1]}
    
    mock_outputs = MagicMock()
    mock_outputs.logits = torch.tensor([[0.1, 0.9]])
    mock_model.return_value = mock_outputs

    result = await check_text("Test input")
    
    assert result == {
        'text': "Test input",
        'excluded': True,
        'topic': "example_topic"
    }
    mock_tokenizer.assert_called_once_with("Test input", return_tensors="pt", padding=True, truncation=True, max_length=512)
    mock_model.assert_called_once_with(**{"input_ids": [0], "attention_mask": [1]})

