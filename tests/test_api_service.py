# test_api_service.py
import pytest
from fastapi.testclient import TestClient
from api_service import app, TrainingData

# Creating a test client
client = TestClient(app)

# Mocking the datacollection module and its function
class MockDataCollection:
    @staticmethod
    def add_data(text, label):
        return "Data added successfully"

# Patching the datacollection module in the api_service
def test_receive_training_data(monkeypatch):
    # Replacing the datacollection module with the mock
    monkeypatch.setattr("api_service.data_collection", MockDataCollection)

    # Sample data for testing
    test_data = {
        "text": "Sample text",
        "label": 1
    }

    # Making a post request to the /trainingday/ endpoint
    response = client.post("/trainingday/", json=test_data)

    # Checking the response status code
    assert response.status_code == 200

    # Checking the response message
    assert response.json() == {"message": "Data added successfully"}

def test_invalid_data():
    # Invalid test data (missing 'label')
    invalid_data = {
        "text": "Sample text"
    }

    # Making a post request to the /trainingday/ endpoint
    response = client.post("/trainingday/", json=invalid_data)

    # Checking the response status code for validation error
    assert response.status_code == 422
