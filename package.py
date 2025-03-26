from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ollama
import base64
from io import BytesIO
from PIL import Image
import requests

# Initialize Ollama client
client = ollama.Client()

# FastAPI app setup
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to AI Wardrobe!"}

# Endpoint for text suggestions
@app.post("/api/generate-suggestions")
async def generate_suggestions(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "What should I wear today?")
    
    model = "llama2"  # Replace with your preferred model in Ollama
    try:
        response = client.generate(model=model, prompt=user_input)
        suggestions = response.response.strip()
        return {"message": suggestions}
    except Exception as e:
        return {"error": str(e)}

# Endpoint for image generation
@app.post("/api/generate-image")
async def generate_image(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "Generate a clothing suggestion image")
    
    # Replace this with your image-generation service or model
    try:
        # Example using placeholder API
        dalle_response = client.generate(model="dalle-mini", prompt=prompt)
        
        # Generate image as base64 (for demo purpose)
        if dalle_response.response:
            image_url = dalle_response.response.strip()  # Assuming URL is returned
            return {"image_url": image_url}
        else:
            return {"error": "Failed to generate image"}
    except Exception as e:
        return {"error": str(e)}
