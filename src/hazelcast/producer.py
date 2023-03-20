
import hazelcast as hz

N = 100

if __name__ == '__main__':
    client = hz.HazelcastClient()
    q = client.get_queue("queue").blocking()
    q.clear()
    print(f"Queue size: {q.size()}")

    i = 0
    while True:
    # for i in range(N):
        print(f"Putting {i}")
        q.put(i)
        print(f"Remaining capacity after push: {q.remaining_capacity()}")
        i += 1

