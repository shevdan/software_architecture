import hazelcast as hz

from argparse import ArgumentParser

from time import sleep

N = 100

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-pn", "--process_num", help="Number of the process", required=True)
    args = parser.parse_args()
    process_num = args.process_num

    client = hz.HazelcastClient()
    m = client.get_map("map")
    key = "1"

    m.put_if_absent(key, 0).result()

    for _ in range(N):
        m.lock(key).result()
        try:
            value = m.get(key).result()
            sleep(0.01)
            value += 1
            m.put(key, value).result()
        finally:
            m.unlock(key).result()

    print(f"Process number {process_num} operated value {m.get(key).result()}")
    client.shutdown()
