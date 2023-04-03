import uvicorn
from fastapi import FastAPI, Request, Response, status
import requests
import uuid
from pydantic import BaseModel
from config import Config
from random import choice
import argparse
import json

class User(BaseModel):
    message: str

app = FastAPI()

CONF = Config.urls_from_conf()


@app.get('/')
def home():
    print("Facade message. Getting messages")
    try:
        logging_response = requests.get(choice(CONF.logging_url))
        messaging_response = requests.get(CONF.message_url)
    except Exception as e:
        return f"Error connecting to logging and/or message services. Error: {e}"
    if logging_response.status_code != 200:
        return  f"error in logging service: {logging_response.text}"
    if messaging_response.status_code != 200:
        return f"error in message service: {messaging_response.text}"

    return f"{logging_response.text}: {messaging_response.text}"

@app.post("/")
async def post_msg(msg: Request):
    data = await msg.json()
    message = data.get("message")
    print(f"Facade service. Posting message: {message}")
    logging_url = choice(CONF.logging_url)
    messaging_url = CONF.message_url
    data = {
        "message":  message,
        "uuid": str(uuid.uuid4())
        }
    try:
        r = requests.post(url = logging_url, data = json.dumps(data))
        requests.post(url = messaging_url, data = json.dumps(data))
    except requests.exceptions.ConnectionError:
        print("Logging and/or messaging service unavailable")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'facade_service.py',
                    description = 'Allows user to start facade service')
    parser.add_argument('host', type=str, help="host necessary") 
    parser.add_argument('port', type=int, help="port necessary")           # positional argument
    args = parser.parse_args()
    

    print("Running facade service")
    uvicorn.run("facade_service:app", host = args.host, port=args.port, reload=False)
