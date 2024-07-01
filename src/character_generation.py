from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse
from diffusers import StableDiffusionPipeline
import shutil
import uuid

app = FastAPI()

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token="your_huggingface_token")

@app.post("/generate-character/")
async def generate_character(description: str = Form(...), character_name: str = Form(...)):
    """
    Generate an image based on the character description and name provided by the user.
    """
    try:
        # Generate the image
        generated_image = pipe(description, guidance_scale=7.5).images[0]

        # Save the image to a temporary file
        file_path = f"temp_images/{uuid.uuid4()}.png"
        generated_image.save(file_path)
        
        return FileResponse(file_path, media_type='image/png', filename=f"{character_name}.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/adjust-character/")
async def adjust_character(description: str = Form(...), character_name: str = Form(...), guidance_scale: float = Form(7.5)):
    """
    Adjust the generated character image based on further input and guidance scale from the user.
    """
    try:
        # Generate the adjusted image
        adjusted_image = pipe(description, guidance_scale=guidance_scale).images[0]

        # Save the adjusted image to a temporary file
        adjusted_file_path = f"temp_images/{uuid.uuid4()}.png"
        adjusted_image.save(adjusted_file_path)

        return FileResponse(adjusted_file_path, media_type='image/png', filename=f"{character_name}_adjusted.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
