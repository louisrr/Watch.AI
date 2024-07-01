# api_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datacollection  # This import assumes datacollection.py is in the same directory or appropriately installed

app = FastAPI()

class TrainingData(BaseModel):
    text: str
    label: int

@app.post("/trainingday/")
def receive_training_data(data: TrainingData):
    result = data_collection.add_data(data.text, data.label)
    return {"message": result}
