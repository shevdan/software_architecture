import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from constants import KAFKA_MSG_TOPIC, KAFKA_URL
import argparse

import threading
from kafka import KafkaConsumer

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()

MSG_STORAGE = []

@app.get('/')
def home():
    print(f"Messages service. Getting messages. {MSG_STORAGE}")
    return MSG_STORAGE


@app.post("/")
def post_msg(msg: Message):
    return "Not implemented yet."


def msg_loop():
    msg_consumer = KafkaConsumer(KAFKA_MSG_TOPIC,
                                 group_id='my-group0',
                                 bootstrap_servers=KAFKA_URL,
                                 auto_offset_reset='earliest',
                                #  enable_auto_commit=True, 
                                 api_version=(0,11,5)
                                 )
    for msg in msg_consumer:
        m = msg.value.decode()
        print(f"Message service: Got message: {m}")
        MSG_STORAGE.append(m)
        print(MSG_STORAGE)


t = threading.Thread(target=msg_loop)
t.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'message_service.py',
                    description = 'Allows user to start message service')
    parser.add_argument('host', type=str, help="host necessary") 
    parser.add_argument('port', type=int, help="port necessary")           # positional argument
    args = parser.parse_args()
    

    print("Messages service. Running message service")
    uvicorn.run("message_service:app", host = args.host, port=args.port, reload=False)
