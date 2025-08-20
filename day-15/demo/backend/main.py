from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# GET request
@app.get("/hello")
def hello():
    return {"message": "Hello from Kubernetes!"}

# Model for POST data
class Message(BaseModel):
    text: str

# POST request
@app.post("/echo")
def echo(message: Message):
    return {"you_said": message.text}
