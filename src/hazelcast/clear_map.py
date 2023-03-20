
from argparse import ArgumentParser
import hazelcast as hz

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("map_name", help="Number of the process")
    args = parser.parse_args()

    client = hz.HazelcastClient()
    try:
        m = client.get_map(args.map_name)
    except Exception as e:
        print(f"Error: {e}")
    m.clear()
    print(f"Cleared map {args.map_name}")
    client.shutdown()