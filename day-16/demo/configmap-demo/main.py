import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Read environment variable with default
APP_NAME = os.getenv("APP_NAME", "My FastAPI App")
GREETING = os.getenv("GREETING", "Hello from Kubernetes!")

# GET request
@app.get("/hello")
def hello():
    return {"app": APP_NAME, "message": GREETING}

# Model for POST data
class Message(BaseModel):
    text: str

# POST request
@app.post("/echo")
def echo(message: Message):
    return {"you_said": message.text, "app": APP_NAME}
