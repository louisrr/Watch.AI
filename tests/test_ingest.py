import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from my_fastapi_app import app  # Replace with the actual name of your FastAPI app script

client = TestClient(app)

@pytest.fixture
def mock_ingest_data():
    with patch('my_fastapi_app.ingest_data') as mock_task:
        yield mock_task

def test_start_ingestion(mock_ingest_data):
    response = client.post("/ingest/", json={"file_path": "dummy_path.csv"})

    assert response.status_code == 200
    assert response.json() == {"message": "Ingestion started", "file_path": "dummy_path.csv"}
    mock_ingest_data.assert_called_once_with("dummy_path.csv")

# For testing async endpoint with BackgroundTasks
@pytest.mark.asyncio
async def test_start_ingestion_async(mock_ingest_data):
    with patch('my_fastapi_app.BackgroundTasks.add_task') as mock_add_task:
        async with client:
            response = await client.post("/ingest/", json={"file_path": "dummy_path.csv"})
            assert response.status_code == 200
            assert response.json() == {"message": "Ingestion started", "file_path": "dummy_path.csv"}
            mock_add_task.assert_called_once_with(ingest_data, "dummy_path.csv")
