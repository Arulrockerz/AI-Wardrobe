from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

# Initialize FastAPI app
app = FastAPI()

# CORS settings (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake User Database (Replace with a real DB)
fake_users_db = {
    "admin": "password123",
    "user": "testpass"
}

# Ollama client for AI chatbot
client = ollama.Client()

# User Login Model
class UserLogin(BaseModel):
    username: str
    password: str

# **Root Endpoint**
@app.get("/")
def read_root():
    return {"message": "Welcome to AI Wardrobe!"}

# **Login Endpoint**
@app.post("/api/login")
async def login(user: UserLogin):
    if user.username in fake_users_db and fake_users_db[user.username] == user.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# **AI Chatbot Endpoint**
@app.post("/api/generate-suggestions")
async def generate_suggestions(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "What should I wear today?")
    
    model = "llama2"  
    try:
        response = client.generate(model=model, prompt=user_input)
        suggestions = response.response.strip()
        return {"message": suggestions}
    except Exception as e:
        return {"error": str(e)}

# **Run the API**
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

        else:
            return {"error": "Failed to generate image"}
    except Exception as e:
        return {"error": str(e)}
