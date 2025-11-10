from Crypto.Cipher import DES
import time

# Known plaintext and known DES key
plaintext = b'TestData1'
key_known = b'\x00\x01' + b'\x00'*6
cipher = DES.new(key_known, DES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext)

# Brute-force over 16-bit prefix (for demonstration)
start = time.time()
found_key = None
for i in range(1 << 16):
    trial_key = i.to_bytes(2, 'big') + b'\x00'*6
    if DES.new(trial_key, DES.MODE_ECB).encrypt(plaintext) == ciphertext:
        found_key = trial_key
        print(f"Found key: {found_key.hex()}")
        break
elapsed = time.time() - start
print(f"Search completed in {elapsed:.3f} seconds")
