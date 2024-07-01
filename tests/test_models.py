import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from my_models import Base, Video, Annotation  # Replace with the actual name of your models script

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    # Create the database and the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables and clean up the database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    # Create a new database session for a test
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_video(db_session):
    # Create a new video instance
    new_video = Video(title="Test Video", description="This is a test video.")
    db_session.add(new_video)
    db_session.commit()

    # Query the video from the database
    video = db_session.query(Video).first()
    assert video is not None
    assert video.title == "Test Video"
    assert video.description == "This is a test video."

def test_create_annotation(db_session):
    # Create a new video instance
    new_video = Video(title="Test Video with Annotation", description="This video has an annotation.")
    db_session.add(new_video)
    db_session.commit()

    # Create a new annotation for the video
    new_annotation = Annotation(text="This is a test annotation.", video_id=new_video.id)
    db_session.add(new_annotation)
    db_session.commit()

    # Query the annotation from the database
    annotation = db_session.query(Annotation).first()
    assert annotation is not None
    assert annotation.text == "This is a test annotation."
    assert annotation.video_id == new_video.id

def test_video_annotation_relationship(db_session):
    # Create a new video instance
    new_video = Video(title="Test Video for Relationship", description="This video is for testing relationships.")
    db_session.add(new_video)
    db_session.commit()

    # Create a new annotation for the video
    new_annotation = Annotation(text="Relationship annotation.", video_id=new_video.id)
    db_session.add(new_annotation)
    db_session.commit()

    # Query the video and check its annotations
    video = db_session.query(Video).first()
    assert video is not None
    assert len(video.annotations) == 1
    assert video.annotations[0].text == "Relationship annotation."

    # Query the annotation and check its video
    annotation = db_session.query(Annotation).first()
    assert annotation is not None
    assert annotation.video is not None
    assert annotation.video.title == "Test Video for Relationship"
