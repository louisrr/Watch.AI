from celery import Celery
from models import Video, Annotation, SessionLocal
import csv

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def ingest_data(file_path):
    db = SessionLocal()
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                video = Video(title=row['title'].strip(), description=row['description'].strip())
                db.add(video)
                if 'annotation' in row:
                    annotation = Annotation(text=row['annotation'].strip(), video=video)
                    db.add(annotation)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()
