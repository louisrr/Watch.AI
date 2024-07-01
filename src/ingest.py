from fastapi import FastAPI, HTTPException, BackgroundTasks
from celery_worker import ingest_data

app = FastAPI()

@app.post("/ingest/")
async def start_ingestion(file_path: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_data, file_path)
    return {"message": "Ingestion started", "file_path": file_path}
