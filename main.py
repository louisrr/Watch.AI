import sys
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import subprocess

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importing functions from various modules
from TextService import process_text
from UserService import create_user, request_password_reset, change_password
from apiservice import trainingday
from character_generation import generate_character, adjust_character
from ingest import ingest_files
from models import Annotation, Video, SessionLocal
from ner_processing import process_ner
from train_gan import train_gan
from trainroberta import process_roberta
from transformers import transformers_function
from video_compilation import compile_video
from video_processing_service import process_video

# Importing frame generation functions
from frame_generation import (
    load_stylegan3_model, generate_coherent_frames, get_character_profile,
    identify_faces, download_image, add_image_to_frame, get_faces,
    check_speech_in_audio, recognize_faces, apply_wav2lip
)

app = FastAPI()

class UserRequest(BaseModel):
    username: str
    password: str
    email: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordChangeRequest(BaseModel):
    unique_hash: str
    new_password: str

class CharacterRequest(BaseModel):
    name: str
    description: str

class IngestRequest(BaseModel):
    data: str

class TextRequest(BaseModel):
    text: str

@app.post("/create_user/")
async def create_user_endpoint(user: UserRequest):
    try:
        create_user(user.username, user.password, user.email)
        return JSONResponse(status_code=200, content={"message": "User created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/request_password_reset/")
async def request_password_reset_endpoint(request: PasswordResetRequest):
    try:
        request_password_reset(request.email)
        return JSONResponse(status_code=200, content={"message": "Password reset request received"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/change_password/{unique_hash}/")
async def change_password_endpoint(unique_hash: str, request: PasswordChangeRequest):
    try:
        change_password(unique_hash, request.new_password)
        return JSONResponse(status_code=200, content={"message": "Password changed successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/trainingday/")
async def trainingday_endpoint():
    try:
        trainingday()
        return JSONResponse(status_code=200, content={"message": "Training day process started"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-character/")
async def generate_character_endpoint(request: CharacterRequest):
    try:
        character = generate_character(request.name, request.description)
        return JSONResponse(status_code=200, content={"character": character})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/adjust-character/")
async def adjust_character_endpoint(request: CharacterRequest):
    try:
        character = adjust_character(request.name, request.description)
        return JSONResponse(status_code=200, content={"character": character})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ingest/")
async def ingest_endpoint(request: IngestRequest):
    try:
        ingest_files(request.data)
        return JSONResponse(status_code=200, content={"message": "Data ingested successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/process_text/")
async def process_text_endpoint(request: TextRequest):
    try:
        result = process_text(request.text)
        return JSONResponse(status_code=200, content={"result": result})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate_frames":
        import argparse
        parser = argparse.ArgumentParser(description='Generate frames using StyleGAN3.')
        parser.add_argument('--model_path', type=str, required=True, help='Path to the StyleGAN3 model file.')
        parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the generated frames.')
        parser.add_argument('--num_frames', type=int, default=30, help='Number of frames to generate.')
        parser.add_argument('--truncation_psi', type=float, default=0.5, help='Truncation psi value for StyleGAN3.')
        
        args = parser.parse_args()

        # Load StyleGAN3 model
        G = load_stylegan3_model(args.model_path)
        
        # Generate coherent frames
        generate_coherent_frames(G, args.output_dir, num_frames=args.num_frames, truncation_psi=args.truncation_psi)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)