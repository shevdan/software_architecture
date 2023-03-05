import uvicorn
from fastapi import FastAPI
import requests
import uuid
from pydantic import BaseModel

class User(BaseModel):
    message: str

app = FastAPI()


@app.get('/')
def home():
    try:
        logging_response = requests.get("http://127.0.0.1:8082/")
        messaging_response = requests.get("http://127.0.0.1:8083/")
    except requests.exceptions.ConnectionError:
        return "Error connecting to logging and/or message services"
    return f"{logging_response.text} : {messaging_response.text}"

@app.post("/")
def post_msg(msg: User):
    message = msg.message
    logging_url = "http://127.0.0.1:8082"
    messaging_url = "http://127.0.0.1:8083/"
    data = {
        "message":  message,
        "uuid": str(uuid.uuid4())
        }
    try:
        r = requests.post(url = logging_url, json = data)
        print(r.status_code)
        requests.post(url = messaging_url, json = data)
        print(r.status_code)
    except requests.exceptions.ConnectionError:
        print("Logging and/or messaging service unavailable")


if __name__ == "__main__":
    uvicorn.run("facade_service:app", port=8080, reload=False)
