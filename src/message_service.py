import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import argparse

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()

@app.get('/')
def home():
    print("Messages service. Getting messages.")
    return "Not implemented yet."


@app.post("/")
def post_msg(msg: Message):
    return "Not implemented yet."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'message_service.py',
                    description = 'Allows user to start message service')
    parser.add_argument('host', type=str, help="host necessary") 
    parser.add_argument('port', type=int, help="port necessary")           # positional argument
    args = parser.parse_args()
    

    print("Messages service. Running message service")
    uvicorn.run("message_service:app", host = args.host, port=args.port, reload=False)
