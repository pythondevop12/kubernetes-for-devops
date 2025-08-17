import logging

# Configure logging to write to /var/log/app.log
logging.basicConfig(
    filename="/var/log/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello")
def hello():
    logging.info("Hello endpoint was called")
    return {"message": "Hello from Kubernetes!"}

class Message(BaseModel):
    text: str

@app.post("/echo")
def echo(message: Message):
    logging.info(f"Echo received: {message.text}")
    return {"you_said": message.text}
