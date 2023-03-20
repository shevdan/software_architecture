import requests
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'cli.py',
                    description = 'Allows user to send post and get requests to facade service')
    parser.add_argument('method', type=str, help="Http method. Either post or get")           # positional argument
    parser.add_argument('-m', '--message', type=str, default="", help="Message to post request. Default is empty string")      # option that takes a value


    args = parser.parse_args()
    if args.method not in ["post", "get"]:
        raise ValueError("Wrong method type")
    facade_url = "http://127.0.0.1:8080/"
    if args.method == "post":
        data = {
            "message": args.message
        }
        requests.post(url = facade_url, json = data)
    else:
        r = requests.get(facade_url)
        print(r.json())
