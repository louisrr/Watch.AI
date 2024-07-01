# test_ingest_data.py
import pytest
from unittest.mock import mock_open, patch, MagicMock
from celery import Celery
from my_celery_app import ingest_data, Video, Annotation

# Mock database session
class MockSession:
    def __init__(self):
        self.added_objects = []
        self.committed = False

    def add(self, obj):
        self.added_objects.append(obj)

    def commit(self):
        self.committed = True

    def close(self):
        pass

@pytest.fixture
def celery_app(celery_config):
    celery_app = Celery('tasks', broker='memory://', backend='rpc://')
    celery_app.conf.update(celery_config)
    return celery_app

@pytest.fixture
def celery_worker(celery_app, celery_includes):
    return celery_app.Worker(includes=celery_includes)

def test_ingest_data_success(monkeypatch):
    # Mock CSV file content
    mock_csv_content = """title,description,annotation
                          Sample Title 1,Sample Description 1,Sample Annotation 1
                          Sample Title 2,Sample Description 2,
                          Sample Title 3,Sample Description 3,Sample Annotation 3"""

    # Mock the open function to read the CSV content
    mock_open_instance = mock_open(read_data=mock_csv_content)
    monkeypatch.setattr("builtins.open", mock_open_instance)

    # Mock the database session
    mock_session = MockSession()
    monkeypatch.setattr("my_celery_app.SessionLocal", lambda: mock_session)

    # Run the Celery task
    ingest_data("dummy_path.csv")

    # Verify the data was ingested correctly
    assert len(mock_session.added_objects) == 5  # 3 videos + 2 annotations
    assert mock_session.committed == True

def test_ingest_data_exception(monkeypatch):
    # Mock CSV file content with missing 'title' field to cause an exception
    mock_csv_content = """title,description,annotation
                          ,Sample Description 1,Sample Annotation 1"""

    # Mock the open function to read the CSV content
    mock_open_instance = mock_open(read_data=mock_csv_content)
    monkeypatch.setattr("builtins.open", mock_open_instance)

    # Mock the database session
    mock_session = MockSession()
    monkeypatch.setattr("my_celery_app.SessionLocal", lambda: mock_session)

    # Mock print to verify exception message
    mock_print = MagicMock()
    monkeypatch.setattr("builtins.print", mock_print)

    # Run the Celery task
    ingest_data("dummy_path.csv")

    # Verify the exception was caught and printed
    mock_print.assert_called_with("An error occurred: 'title'")

    # Verify no data was committed
    assert mock_session.committed == False
