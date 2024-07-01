# WatchAI

## What is WatchAI
WatchAI is an AI video generation service that allows users to generate 2K video scenes up to 2 minutes or 120 seconds in length with specific life-like, human characters, backdrops, background music. Public figures and people who have requested to not be used in generated videos are not able to be cast as characters in generated video unless they have granted expressed, and legally verifiable permission. 

# Mathematical Concepts for Video Processing and Compilation

## 1. Video Frame Extraction
To extract frames from a video, we sample a sequence at regular intervals.

![Equation1](https://latex.codecogs.com/svg.latex?V(t)\quad%20\text{is%20the%20video%20as%20a%20function%20of%20time}%20t.)

To extract frames, we sample \( V \) at intervals \( \Delta t \):

![Equation2](https://latex.codecogs.com/svg.latex?\{V(t_0),%20V(t_0%20+%20\Delta%20t),%20V(t_0%20+%202\Delta%20t),%20\ldots\})

## 2. Frame Processing (e.g., resizing, filtering)
This involves applying transformations to each frame, often represented as matrices.

![Equation3](https://latex.codecogs.com/svg.latex?F\quad%20\text{is%20a%20frame,%20and}%20T%20\text{is%20a%20transformation%20matrix.})

The transformed frame \( F' \) is given by:

![Equation4](https://latex.codecogs.com/svg.latex?F'%20=%20T%20\cdot%20F)

## 3. Optical Flow
Optical flow calculation involves determining the motion between two frames by comparing pixel intensities.

![Equation5](https://latex.codecogs.com/svg.latex?I(x,%20y,%20t)\quad%20\text{represents%20the%20intensity%20of%20the%20pixel%20at%20position}\;%20(x,%20y)\;%20\text{at%20time}\;%20t.)

The optical flow vector \( (u, v) \) is the solution to:

![Equation6](https://latex.codecogs.com/svg.latex?I(x%20+%20u,%20y%20+%20v,%20t%20+%201)\approx%20I(x,%20y,%20t))

Approximated by:

![Equation7](https://latex.codecogs.com/svg.latex?\frac{\partial%20I}{\partial%20x}%20u%20+%20\frac{\partial%20I}{\partial%20y}%20v%20+%20\frac{\partial%20I}{\partial%20t}%20=%200)

## 4. Background Subtraction
Background subtraction is used to separate foreground objects from the background in video frames.

![Equation8](https://latex.codecogs.com/svg.latex?I_t(x,%20y)\quad%20\text{is%20the%20pixel%20intensity%20at%20time}\;%20t,%20\;%20B(x,%20y)\;%20\text{is%20the%20background%20model.})

The foreground mask \( F_t(x, y) \) is given by:

![Equation9](https://latex.codecogs.com/svg.latex?F_t(x,%20y)%20=%20|%20I_t(x,%20y)%20-%20B(x,%20y)%20|%20>%20\text{threshold})

## 5. Motion Detection
Motion detection involves identifying changes between consecutive frames to detect movement.

![Equation10](https://latex.codecogs.com/svg.latex?F_t\quad%20\text{and}\;%20F_{t+1}\;%20\text{are%20consecutive%20frames.})

The difference frame \( D \) is:

![Equation11](https://latex.codecogs.com/svg.latex?D%20=%20|%20F_{t+1}%20-%20F_t%20|)

Motion is detected if \( D \) exceeds a threshold.

## 6. Video Writing
To compile the processed frames back into a video, we write each frame in sequence to a video file.

![Equation12](https://latex.codecogs.com/svg.latex?\{F'_i\}\quad%20\text{is%20the%20sequence%20of%20processed%20frames.})

The compiled video \( V' \) is:

![Equation13](https://latex.codecogs.com/svg.latex?V'%20=%20\{F'_0,%20F'_1,%20F'_2,%20\ldots,%20F'_n\})

## Installation
- Install Python 3.0+ on your machine
- CD into the main directory or, `/f/watch.ai/watchai`
- pip install fastapi uvicorn passlib[argon2] cassandra-driver
- pip install fastapi uvicorn fairseq transformers
- pip install transformers torch

# Training RoBERTa with FastAPI Integration
This project provides a modular framework for training a RoBERTa model to classify text. It includes scripts for data collection, an API service for dynamic data ingestion, and a training module. Follow the instructions below to set up and run the training environment.

## Prerequisites

Before you start, ensure you have the following installed:

* Python 3.8 or newer
* pip (Python package installer)
* Git (optional, for version control)

## Environment Setup

1. **Clone the Repository** (optional if you have direct access to the files)
```
git clone git@github.com:louisrr/Watch.AI.git
cd watchai
```

2. **Create a Python Virtual Environment**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Required Packages**
```
pip install torch transformers fastapi uvicorn
```

## Project Structure

* **datacollection.py:** Handles dynamic data collection and dataset management.
* **apiservice.py:** FastAPI application for handling API requests.
* **trainroberta.py:** Script for training the RoBERTa model.

## Usage

## Starting the Data Collection API

1. **Start the FastAPI server** to begin receiving data through the API.
```
uvicorn apiservice:app --reload
```

## Sending Data for Training
1. **Send POST requests** to the API to add new training data. You can use **curl**,
Postman, or any HTTP client:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/trainingday/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Sample text for classification",
  "label": 0
}'
```

## Training the Model
1. **Run the training script once** once you have collected enough data.
```
python trainroberta.py
```

## Configuration
* **Model and Tokenizer:** The scripts use **roberta-base**. You can change this by modifying the import statement in **trainroberta.py** and **datacollection.py**.
* **Data Handling:** Adjust the batch size and number of epochs in **trainroberta.py** based on your system's capability and the dataset size.

## Maintaining the System
* Regularly update the dependencies to their latest versions to mitigate security risks and improve performance:
```
pip install --upgrade torch transformers fastapi uvicorn
```
* **Monitor the API** using tools like Prometheus or Grafana for insights into request loads and performance.
* If model training does not start, check the dataset size and ensure it is not empty.

## TBD Additions 
Things this project needs are below so if you're feeling like a super hero LET'S GO! 
* **WatchAI Command Line Interface (CLI):** We need control features in the CLI that includes the following:
  * Official branding message with ASCII art in the terminal
  * Add data to the dataset for the RoBERTa from the terminal
  * Access RoBERTa from the terminal 
  * Remove data from the RoBERTa model from the terminal 
  * Return a list of prompts from the terminal
  * Enter a video link into the terminal, and to add the video to the training model
  * Search **Pipeline** 
  * Return a list of **Pipeline** groups
  * Find **Pipeline** group, by group_id
  * Start a mapReduce in **Pipeline**
  * Remove **Pipeline** by group_id
  * Enter **Pipeline** Query Language statement
  * Add dataset to RoBERTa 
  * Train RoBERTa model on dataset(s)
  * Delete RoBERTa dataset(s), model(s) by ID
  * Add/Remove video generation/GAN/transformer dataset(s)
  * Add/Remove video generation/GAN/transformer model(s)
  * Train video generation/GAN/transformer model (or by ID)
  * STITCH {Video ID} + {Video ID} ... TO {output path} ? {URL}
  * Developer names in credits
  * Data Collection System controls
  * Web Crawler Controls
  * Image/Video Enhancement Controls
  * Audio Controls/settings
  * Data Preparation Service controls

* **Movie Scene Generative Adversarial Network/Transformer:** With high resolution/quality photo with:
  * Shutter speed settings (simulated)
  * Cammera Lens appearance settings (simulated) 
  * Color settings
  * Character settings
  * Background/Scenery settings

* **Image Enhancement GAN (for video):** We can crawl the Internet for videos and upscale them to 4K.
  * Evaluate **BSRGAN**: Designing a Practical Degradation Model for Deep Blind Image Super-Resolution **[paper]** https://arxiv.org/pdf/2103.14006.pdf **[code]** https://github.com/cszn/BSRGAN
  * Evaluate **FastDVDnet**: A state-of-the-art, simple and fast network for Deep Video Denoising which uses no motion compensation. https://github.com/m-tassano/fastdvdnet
  * Evaluate Kai Zhang's denoising tool **[code]** https://github.com/cszn/SCUNet

* **Data Collection System (DCS): ** 
  * **Web Crawler:** Crawl the Internet, in search of (x), feed to data preparation service 
  * **Data Preparation Service:** Take data from the crawler clean to for (x,y) 
  * **Point For X:** Search for photos, video, and data from a specific longitude/latitude
  * DONE! Data Collection System -->> DARK SCAN with more capability
