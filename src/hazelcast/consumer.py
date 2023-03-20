
from argparse import ArgumentParser
import hazelcast as hz


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-pn", "--process_num", help="Number of the process", required=True)
    args = parser.parse_args()


    client = hz.HazelcastClient()
    q = client.get_queue("queue")

    while True:
        value = q.poll().result()
        if value is None:
            continue
        print(f"Consumer {args.process_num} poll {value}")
