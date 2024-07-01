# test_fastapi_app.py
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from my_fastapi_app import app, sanitize  # Replace with the actual name of your FastAPI app script

client = TestClient(app)

@pytest.fixture
def mock_cassandra():
    with patch('my_fastapi_app.Cluster') as MockCluster, \
         patch('my_fastapi_app.PlainTextAuthProvider') as MockAuthProvider:
        
        mock_session = MagicMock()
        mock_cluster = MockCluster.return_value
        mock_cluster.connect.return_value = mock_session
        
        yield mock_session

def test_sanitize():
    assert sanitize("hello@world.com") == "hello@world.com"
    assert sanitize("hello@world.com!") == "hello@world.com"
    assert sanitize("hello@world!.com") == "hello@world.com"
    assert sanitize("hello@world.com;") == "hello@world.com"

@pytest.mark.asyncio
async def test_create_user(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = None
    
    response = client.post("/create_user/", json={"email": "test@example.com", "password": "password123"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_create_user_existing_email(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = {"user_email": "test@example.com"}
    
    response = client.post("/create_user/", json={"email": "test@example.com", "password": "password123"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_request_password_reset(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = {"user_email": "test@example.com"}
    
    response = client.post("/request_password_reset/", json={"email": "test@example.com"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset requested"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_request_password_reset_email_not_found(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = None
    
    response = client.post("/request_password_reset/", json={"email": "test@example.com"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_change_password(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = {
        "hash": "some_hash",
        "expiry": "2099-01-01T00:00:00Z",  # Future expiry date
        "request_ip": "user_ip_address",
        "change_key": "123456",
        "original_email": "test@example.com"
    }
    
    response = client.post("/change_password/some_hash/", json={"change": "123456", "new_password": "newpassword123"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Password successfully updated"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_change_password_invalid_link(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = None
    
    response = client.post("/change_password/some_hash/", json={"change": "123456", "new_password": "newpassword123"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid reset link"}
    mock_session.execute.assert_called()

@pytest.mark.asyncio
async def test_change_password_expired(mock_cassandra):
    mock_session = mock_cassandra
    
    # Mock database responses
    mock_session.execute.return_value.one.return_value = {
        "hash": "some_hash",
        "expiry": "2000-01-01T00:00:00Z",  # Past expiry date
        "request_ip": "user_ip_address",
        "change_key": "123456",
        "original_email": "test@example.com"
    }
    
    response = client.post("/change_password/some_hash/", json={"change": "123456", "new_password": "newpassword123"})
    
    assert response.status_code == 200
    assert response.text == "This key is expired. Please use the password reset function again."
    mock_session.execute.assert_called()

