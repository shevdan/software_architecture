import hazelcast as hz
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--put", help="Flag whether to put values. True by default", action = "store_false")
    parser.add_argument("-l", "--loss_check", help="Flag whether to check for data integrity", action = "store_true")
    args = parser.parse_args()


    client = hz.HazelcastClient()
    m = client.get_map("m1").blocking()

    if args.loss_check:
        lost_counter = 0
        for i in range(1000):
            if m.get(i) is None:
                lost_counter += 1
        print(f"Lost {lost_counter}/{1000} entries")

    if args.put:
        for i in range(1000):
            m.put(i, f"Item value: {i}")
    
    client.shutdown()
    
