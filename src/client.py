import requests
import argparse
# from config import Config
import json
# CONF = Config.urls_from_conf()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'cli.py',
                    description = 'Allows user to send post and get requests to facade service')
    parser.add_argument('method', type=str, help="Http method. Either post or get")           # positional argument
    parser.add_argument('-m', '--message', type=str, default="", help="Message to post request. Default is empty string")      # option that takes a value


    args = parser.parse_args()
    if args.method not in ["post", "get"]:
        raise ValueError("Wrong method type")
    if args.method == "post":
        data = {
            "message": args.message
        }
        requests.post(url = f"http://127.0.0.1:8081", data = json.dumps(data))
    else:
        r = requests.get(f"http://127.0.0.1:8081")
        print(r.json())
