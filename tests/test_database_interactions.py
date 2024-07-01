import pytest
from unittest.mock import patch, MagicMock
from my_script import connect_to_db, get_visual_representation

@pytest.fixture
def mock_cluster():
    with patch('my_script.Cluster') as MockCluster:
        mock_session = MagicMock()
        mock_cluster = MagicMock()
        mock_cluster.connect.return_value = mock_session
        MockCluster.return_value = mock_cluster
        yield mock_session

def test_connect_to_db(mock_cluster):
    session = connect_to_db()
    assert session is not None
    assert mock_cluster.connect.called
    assert mock_cluster.connect.call_args[0] == ('your_keyspace',)

def test_get_visual_representation_success(mock_cluster):
    entity = 'test_entity'
    mock_result = MagicMock()
    mock_result.one.return_value = MagicMock(visual_link='http://example.com/image.png')
    mock_cluster.execute.return_value = mock_result

    visual_link = get_visual_representation(entity, mock_cluster)

    assert visual_link == 'http://example.com/image.png'
    mock_cluster.execute.assert_called_once_with("SELECT visual_link FROM visual_elements WHERE name = %s", (entity,))

def test_get_visual_representation_no_result(mock_cluster):
    entity = 'test_entity'
    mock_cluster.execute.return_value = None

    visual_link = get_visual_representation(entity, mock_cluster)

    assert visual_link is None
    mock_cluster.execute.assert_called_once_with("SELECT visual_link FROM visual_elements WHERE name = %s", (entity,))

def test_get_visual_representation_empty_result(mock_cluster):
    entity = 'test_entity'
    mock_result = MagicMock()
    mock_result.one.return_value = None
    mock_cluster.execute.return_value = mock_result

    visual_link = get_visual_representation(entity, mock_cluster)

    assert visual_link is None
    mock_cluster.execute.assert_called_once_with("SELECT visual_link FROM visual_elements WHERE name = %s", (entity,))
