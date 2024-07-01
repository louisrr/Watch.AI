import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from my_fastapi_app import app  # Import your FastAPI app

# Creating a test client
client = TestClient(app)

@pytest.fixture
def mock_pipe():
    with patch("my_fastapi_app.StableDiffusionPipeline.from_pretrained") as mock_model:
        mock_instance = MagicMock()
        mock_instance.return_value = MagicMock()
        mock_instance.return_value.images = [MagicMock()]
        mock_instance.return_value.images[0].save = MagicMock()
        mock_model.return_value = mock_instance
        yield mock_instance

def test_generate_character_success(mock_pipe):
    response = client.post(
        "/generate-character/",
        data={"description": "A fantasy character", "character_name": "FantasyHero"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_adjust_character_success(mock_pipe):
    response = client.post(
        "/adjust-character/",
        data={"description": "A futuristic character", "character_name": "FutureHero", "guidance_scale": 8.5},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_generate_character_exception(mock_pipe, monkeypatch):
    def mock_generate(*args, **kwargs):
        raise Exception("Mocked exception")

    mock_pipe.return_value.__call__.side_effect = mock_generate

    response = client.post(
        "/generate-character/",
        data={"description": "A fantasy character", "character_name": "FantasyHero"},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Mocked exception"}

def test_adjust_character_exception(mock_pipe, monkeypatch):
    def mock_adjust(*args, **kwargs):
        raise Exception("Mocked exception")

    mock_pipe.return_value.__call__.side_effect = mock_adjust

    response = client.post(
        "/adjust-character/",
        data={"description": "A futuristic character", "character_name": "FutureHero", "guidance_scale": 8.5},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Mocked exception"}
