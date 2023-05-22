from typing import Dict, List, Union, Any

import yaml
from constants import LOGGING, MESSAGE, FACADE
from dataclasses import dataclass
import json

from consul import Consul

def get_config(consul: Consul, key: str, default_value: Any):
    _, value = consul.kv.get(key)
    print(f"Retrieving value from key {key}. Obtained: {value}.")
    if value is None:
        print(f"Value is None. Putting default value {default_value}.")
        consul.kv.put(key, json.dumps(default_value))
        return default_value
    return json.loads(value["Value"].decode("ascii"))



# @dataclass
# class Config:
#     facade_url: str
#     logging_url: list
#     message_url: str

#     @staticmethod
#     def urls_from_conf(path: str = "services_conf.yml"):
#         config: Dict = yaml.safe_load(open(path, 'r'))
#         return Config(
#             Config.__convert_to_url(config[FACADE]),
#             Config.__convert_to_url(config[LOGGING]),
#             Config.__convert_to_url(config[MESSAGE]),
#         )

#     @staticmethod
#     def __convert_to_url(service_ports: Union[Dict, List[Dict]]) -> Union[List, str]:
#         if isinstance(service_ports, list):
#             return [f"http://{subports['host']}:{subports['port']}" for subports in service_ports]
#         if isinstance(service_ports, dict):
#             return f"http://{service_ports['host']}:{service_ports['port']}"
#         raise ValueError("Bad service type") 

