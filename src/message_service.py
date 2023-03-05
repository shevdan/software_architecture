import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()

@app.get('/')
def home():
    return "Not implemented yet."


@app.post("/")
def post_msg(msg: Message):
    return "Not implemented yet."


if __name__ == "__main__":
    uvicorn.run("message_service:app", port=8083, reload=False)
