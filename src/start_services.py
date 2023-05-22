import os
import subprocess
from argparse import ArgumentParser, Namespace
from typing import Dict, Optional

import yaml

from constants import FACADE, LOGGING, MESSAGE
from consul import Consul
import json



def start_service(args: Namespace):
    selected_service: Optional[str] = None
    if args.facade:
        if args.logging or args.message:
            raise ValueError("Only one service to start at a time")
        selected_service = FACADE
    elif args.logging:
        if args.message:
            raise ValueError("Only one service to start at a time")
        selected_service = LOGGING
    elif args.message:
        selected_service = MESSAGE
    else:
        raise ValueError("Only one service to start at a time")
    
    consul = Consul()

    url = f"http://{args.host}:{args.port}"
    if args.number is None:
        service_json_url = json.dumps(url)
    else:
        _, urls = consul.kv.get(selected_service)
        current_service_url = {f"{selected_service}_{args.number}": url}
        if urls is None:
            service_json_url = json.dumps(current_service_url)
        else:
            urls_dict = json.loads(urls['Value'].decode('ascii'))
            urls_dict.update(current_service_url)
            service_json_url = json.dumps(urls_dict)
    print(f"Pushing key-value pair to consul: ({selected_service}, {service_json_url})")
    consul.kv.put(selected_service, service_json_url)


    # try:
    #     if isinstance(config[selected_service], list):
    #         host = config[selected_service][n]['host']
    #         port = config[selected_service][n]['port']
    #     else:
    #         host = config[selected_service]['host']
    #         port = config[selected_service]['port']
    # except IndexError:
    #     print(f"Number {n} for service is out of range for possible ports designated to {selected_service}")

    start_cmd = f"python3 {selected_service}_service.py {args.host} {args.port}"

    consul = Consul()

    subprocess.run(start_cmd, shell=True)


if __name__ == "__main__":
    parser = ArgumentParser(prog = 'start_service.py',
                    description = 'Allows user to start all services')

    parser.add_argument("--config", "-c", type=str, required=False, help="Path to config file. Default: services_conf.yml, assuming it is located in the same working directory",
                        default="services_conf.yml")
    parser.add_argument("--facade", action="store_const", const=True, help="start facade service")
    parser.add_argument("--logging", action="store_const", const=True, help="start logging service")
    parser.add_argument("--message", action="store_const", const=True, help="start message service")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8081)
    parser.add_argument("--number", "-n", type=int, required=False, default=0,
                        help="Number of service in case of replication. Should be used for multiple logging services")

    args = parser.parse_args()

    # config: Dict = yaml.safe_load(open(args.config, 'r'))


    start_service(args)
