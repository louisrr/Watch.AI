# test_scylla_db.py
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid
import my_scylla_script  # Replace with the name of your script

@pytest.fixture
def mock_cluster():
    with patch('my_scylla_script.Cluster') as MockCluster:
        mock_session = MagicMock()
        mock_cluster = MagicMock()
        mock_cluster.connect.return_value = mock_session
        MockCluster.return_value = mock_cluster
        yield mock_session

def test_insert_query_success(mock_cluster, monkeypatch):
    # Mock the datetime and uuid to return fixed values
    fixed_datetime = datetime(2023, 1, 1, 12, 0, 0)
    fixed_uuid = uuid.UUID('12345678123456781234567812345678')
    
    monkeypatch.setattr('my_scylla_script.datetime', MagicMock(now=lambda: fixed_datetime))
    monkeypatch.setattr('my_scylla_script.uuid', MagicMock(uuid4=lambda: fixed_uuid))
    
    # Mock input values
    user_id = 'user123'
    character_name = 'AvatarName'
    image_url = 'http://example.com/avatar.png'

    # Execute the script
    my_scylla_script.insert_character_profile(user_id, character_name, image_url)  # Ensure your function accepts parameters
    
    # Verify the query was executed correctly
    expected_query = f"""
    INSERT INTO your_keyspace_name.character_profiles (character_id, user_id, name, image_url, created_at)
    VALUES (%s, %s, %s, %s, %s);
    """
    mock_cluster.execute.assert_called_once_with(expected_query, (fixed_uuid, user_id, character_name, image_url, fixed_datetime))

def test_insert_query_exception(mock_cluster, monkeypatch):
    # Mock the datetime and uuid to return fixed values
    fixed_datetime = datetime(2023, 1, 1, 12, 0, 0)
    fixed_uuid = uuid.UUID('12345678123456781234567812345678')
    
    monkeypatch.setattr('my_scylla_script.datetime', MagicMock(now=lambda: fixed_datetime))
    monkeypatch.setattr('my_scylla_script.uuid', MagicMock(uuid4=lambda: fixed_uuid))
    
    # Mock input values
    user_id = 'user123'
    character_name = 'AvatarName'
    image_url = 'http://example.com/avatar.png'

    # Mock the execute method to raise an exception
    mock_cluster.execute.side_effect = Exception("Mocked exception")
    
    # Run the function and assert it raises an exception
    with pytest.raises(Exception) as excinfo:
        my_scylla_script.insert_character_profile(user_id, character_name, image_url)  # Ensure your function accepts parameters

    assert "Mocked exception" in str(excinfo.value)

