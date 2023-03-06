
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    uuid: str


app = FastAPI()

MSG_HASH_MAP = {}


@app.get('/')
def home():
    return "; ".join(MSG_HASH_MAP.values())


@app.post("/")
def post_msg(msg: Message):
    print(f"Obtained {msg.uuid}: {msg.message}")
    MSG_HASH_MAP[msg.uuid] = msg.message


if __name__ == "__main__":
    print("Running logging service")
    uvicorn.run("logging_service:app", port=8082, reload=False)
