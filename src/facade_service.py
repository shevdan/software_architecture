import uvicorn
from fastapi import FastAPI, Request, Response, status
import requests
import uuid
from pydantic import BaseModel
from random import choice
import argparse
import json
from kafka import KafkaProducer
from consul import Consul
from constants import KAFKA_CONFIG_KEY, DEFAULT_KAFKA_CONFIG, LOGGING, MESSAGE
from config import get_config

class User(BaseModel):
    message: str

app = FastAPI()

consul = Consul()
config = get_config(consul, KAFKA_CONFIG_KEY, DEFAULT_KAFKA_CONFIG)
msg_producer = KafkaProducer(bootstrap_servers=config["url"], api_version=(0,11,5))

def get_url(consul, key):
    return choice(list(json.loads(consul.kv.get(key)[1]['Value'].decode('ascii')).values()))


@app.get('/')
def home():
    print("Facade message. Getting messages")
    try:
        logging_url = get_url(consul, LOGGING)
        message_url = get_url(consul, MESSAGE)
        logging_response = requests.get(logging_url)
        messaging_response = requests.get(message_url)
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
    logging_url = get_url(consul, LOGGING)
    data = {
        "message":  message,
        "uuid": str(uuid.uuid4())
        }
    try:
        h = msg_producer.send(config["topic"], message.encode('utf-8'))
        metadata = h.get(timeout=10)
        print(f"Message metadata: {metadata.topic}; {metadata.partition}; {metadata.offset}")
        msg_producer.flush()
        r = requests.post(url = logging_url, data = json.dumps(data))
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
