import pytest
from unittest.mock import patch, MagicMock
from my_script import setup_ner_pipeline, perform_ner  # Replace with the actual name of your script

@pytest.fixture
def mock_transformers():
    with patch('my_script.RobertaTokenizer') as MockTokenizer, \
         patch('my_script.RobertaForTokenClassification') as MockModel, \
         patch('my_script.pipeline') as MockPipeline:
        
        mock_tokenizer = MockTokenizer.from_pretrained.return_value
        mock_model = MockModel.from_pretrained.return_value
        mock_pipeline = MockPipeline.return_value
        
        yield mock_tokenizer, mock_model, mock_pipeline

def test_setup_ner_pipeline(mock_transformers):
    mock_tokenizer, mock_model, mock_pipeline = mock_transformers
    
    ner_pipeline = setup_ner_pipeline()
    
    assert ner_pipeline == mock_pipeline
    mock_tokenizer.from_pretrained.assert_called_once_with('roberta-base')
    mock_model.from_pretrained.assert_called_once_with('roberta-base-finetuned-ner')
    mock_pipeline.assert_called_once_with(
        "ner", model=mock_model, tokenizer=mock_tokenizer, device=0 if torch.cuda.is_available() else -1
    )

def test_perform_ner(mock_transformers):
    mock_tokenizer, mock_model, mock_pipeline = mock_transformers
    mock_pipeline.return_value = [{"entity": "B-PER", "score": 0.99, "index": 1, "word": "John", "start": 0, "end": 4}]
    
    text = "John is a person."
    ner_results = perform_ner(text)
    
    assert ner_results == [{"entity": "B-PER", "score": 0.99, "index": 1, "word": "John", "start": 0, "end": 4}]
    mock_pipeline.assert_called_once_with(text)

