import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Config from environment variables
APP_NAME = os.getenv("APP_NAME", "My FastAPI App")
GREETING = os.getenv("GREETING", "Hello from Kubernetes!")

# Secrets (these would come from Kubernetes Secret)
DB_USER = os.getenv("DB_USER", "default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_pass")

@app.get("/hello")
def hello():
    return {
        "app": APP_NAME,
        "message": GREETING,
        "db_user": DB_USER,
        "db_password": DB_PASSWORD  # (only for demo, never return passwords in prod!)
    }

class Message(BaseModel):
    text: str

@app.post("/echo")
def echo(message: Message):
    return {
        "you_said": message.text,
        "app": APP_NAME,
        "db_user": DB_USER
    }
