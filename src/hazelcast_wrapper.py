import subprocess
import os
import time
import hazelcast


class HazelcastInstancetWrapper:
    def __init__(self, hz_proc):
        self.hz_proc: subprocess.Popen = hz_proc
        self.hz_client = hazelcast.HazelcastClient()

    def get_map(self, name: str):
        return self.hz_client.get_map(name)

    def __del__(self):
        self.hz_client.shutdown()
        time.sleep(5)
        self.hz_proc.terminate()


class HazelcastWrapper:
    @staticmethod
    def newHazelCastInstance() -> HazelcastInstancetWrapper:
        proc = subprocess.Popen("./start_hz.sh")
        return HazelcastInstancetWrapper(hz_proc=proc)
