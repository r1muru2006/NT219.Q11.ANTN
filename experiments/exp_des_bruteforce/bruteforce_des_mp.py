from Crypto.Cipher import DES
from multiprocessing import Process, Queue, cpu_count
import time, os

plaintext = b'TestData1'
# The known key used to generate demo ciphertext (8 bytes)
known_key = b'\x00\x01' + b'\x00'*6
ciphertext = DES.new(known_key, DES.MODE_ECB).encrypt(plaintext)

def worker(start, step, limit, q):
    for i in range(start, limit, step):
        trial_key = i.to_bytes(2, 'big') + b'\x00'*6
        if DES.new(trial_key, DES.MODE_ECB).encrypt(plaintext) == ciphertext:
            q.put(trial_key.hex())
            return

if __name__ == "__main__":
    CORES = max(1, cpu_count() - 0)
    LIMIT = 1 << 16  # demo limit (2^16)
    q = Queue()
    procs = []
    t0 = time.time()
    for s in range(CORES):
        p = Process(target=worker, args=(s, CORES, LIMIT, q))
        p.start()
        procs.append(p)
    found = None
    try:
        found = q.get(timeout=10)
    except:
        pass
    for p in procs:
        p.terminate()
    print("Found:", found)
    print("Elapsed:", time.time() - t0)
