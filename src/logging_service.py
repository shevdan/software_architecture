
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import argparse
import subprocess
import json
import time
import hazelcast


class HazelcastInstanceWrapper:
    def __init__(self):
        self.hz_proc = subprocess.Popen(["hz", "start"])
        # os.system('./start_hz.sh')
        self.hz_client = hazelcast.HazelcastClient()

    def get_map(self, name: str):
        return self.hz_client.get_map(name)

    def __del__(self):
        self.hz_client.shutdown()
        time.sleep(5)
        self.hz_proc.terminate()


class Message(BaseModel):
    message: str
    uuid: str


app = FastAPI()

# hz_instance = HazelcastInstanceWrapper()
hz_instance = hazelcast.HazelcastClient()
MSG_HASH_MAP = hz_instance.get_map("logging_map")

@app.get('/')
def get_logs():
    print("Logging service. Getting logs")
    return "; ".join(list(MSG_HASH_MAP.values().result()))


@app.post("/")
def post_msg(msg: Message):
    print(f"Logging service. Obtained {msg.uuid}: {msg.message}")
    MSG_HASH_MAP.put(msg.uuid, msg.message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'logging_service.py',
                    description = 'Allows user to start logging service')
    parser.add_argument('host', type=str, help="host necessary") 
    parser.add_argument('port', type=int, help="port necessary")           # positional argument
    args = parser.parse_args()
    

    print("Running logging service")
    uvicorn.run("logging_service:app", host = args.host, port=args.port, reload=False)

