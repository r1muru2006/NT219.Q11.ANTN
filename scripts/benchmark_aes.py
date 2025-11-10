from Crypto.Cipher import AES
import time

key = b'Sixteen byte key'
aes = AES.new(key, AES.MODE_ECB)
plaintext = b'0123456789abcdef'

# Warm-up
_ = aes.encrypt(plaintext)

# Encrypt 1,000,000 blocks to measure throughput
num_blocks = 10**6
start = time.time()
for _ in range(num_blocks):
    aes.encrypt(plaintext)
elapsed = time.time() - start

print(f"Time for {num_blocks} AES encryptions: {elapsed:.2f} seconds")
print(f"Throughput: {num_blocks/elapsed:.1f} ops/s")
