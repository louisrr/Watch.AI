import pytest
from unittest.mock import patch, MagicMock
from transformers import RobertaConfig, RobertaForSequenceClassification

@pytest.fixture
def mock_transformers():
    with patch('your_script.RobertaConfig') as MockConfig, \
         patch('your_script.RobertaForSequenceClassification') as MockModel:
        
        mock_config = MockConfig.from_pretrained.return_value
        mock_model = MockModel.return_value
        
        yield mock_config, mock_model

def test_model_initialization(mock_transformers):
    mock_config, mock_model = mock_transformers
    
    your_num_labels = 2  # Example number of labels
    
    # Import the actual script
    from your_script import model  # Replace with the actual name of your script
    
    # Assertions to check if the configuration and model were initialized correctly
    mock_config.from_pretrained.assert_called_once_with('roberta-base', num_labels=your_num_labels)
    assert isinstance(model, MagicMock), "Model should be an instance of MagicMock"
