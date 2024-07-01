import pytest
from unittest.mock import patch, MagicMock
from my_script import create_frame_specifications  # Replace with the actual name of your script

@pytest.fixture
def mock_db_interactions():
    with patch('my_script.connect_to_db') as mock_connect_to_db, \
         patch('my_script.get_visual_representation') as mock_get_visual_representation:
        
        mock_session = MagicMock()
        mock_connect_to_db.return_value = mock_session
        mock_get_visual_representation.side_effect = lambda word, session: f"http://example.com/{word}.jpg"
        
        yield mock_connect_to_db, mock_get_visual_representation, mock_session

def test_create_frame_specifications(mock_db_interactions):
    mock_connect_to_db, mock_get_visual_representation, mock_session = mock_db_interactions
    
    ner_results = [
        {'word': 'cat', 'entity': 'animal'},
        {'word': 'dog', 'entity': 'animal'}
    ]
    
    expected_frames = [
        {'entity': 'cat', 'type': 'animal', 'visual_link': 'http://example.com/cat.jpg'},
        {'entity': 'dog', 'type': 'animal', 'visual_link': 'http://example.com/dog.jpg'}
    ]
    
    frames = create_frame_specifications(ner_results)
    
    assert frames == expected_frames
    mock_connect_to_db.assert_called_once()
    assert mock_get_visual_representation.call_count == 2
    mock_get_visual_representation.assert_any_call('cat', mock_session)
    mock_get_visual_representation.assert_any_call('dog', mock_session)

