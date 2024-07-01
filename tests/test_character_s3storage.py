# test_s3_upload.py
import boto3
import pytest
from moto import mock_s3
from datetime import datetime
import my_s3_upload_script  # Replace with the name of your script

@pytest.fixture
def s3_client():
    with mock_s3():
        # Create a mock S3 client
        client = boto3.client('s3', region_name='us-east-1')
        # Create a mock S3 bucket
        client.create_bucket(Bucket='your-bucket-name')
        yield client

def test_s3_upload(s3_client, monkeypatch):
    # Mock the datetime to return a fixed timestamp
    fixed_datetime = datetime(2023, 1, 1, 12, 0, 0)
    monkeypatch.setattr('my_s3_upload_script.datetime', lambda: fixed_datetime)

    # Create a temporary file to upload
    temp_file_name = "temp_image.png"
    with open(temp_file_name, 'w') as f:
        f.write("Test image content")

    # Run the upload script
    my_s3_upload_script.upload_file_to_s3()  # Replace with the function name if necessary

    # Check that the file was uploaded
    response = s3_client.list_objects_v2(Bucket='your-bucket-name')
    assert 'Contents' in response
    assert len(response['Contents']) == 1
    assert response['Contents'][0]['Key'] == f"{fixed_datetime.isoformat()}_character.png"

    # Generate the expected URL
    expected_url = f"https://your-bucket-name.s3.amazonaws.com/{fixed_datetime.isoformat()}_character.png"
    assert my_s3_upload_script.image_url == expected_url

def test_s3_upload_exception(s3_client, monkeypatch):
    # Mock the upload_file method to raise an exception
    def mock_upload_file(*args, **kwargs):
        raise Exception("Mocked exception")
    
    monkeypatch.setattr(s3_client, 'upload_file', mock_upload_file)

    with pytest.raises(Exception) as excinfo:
        my_s3_up
