# -------------------LIBRARY-------------------
from pwn import *

# -------------------HIDDEN WARNING-------------------
import warnings
warnings.filterwarnings("ignore", category=BytesWarning)

# -------------------CORE ATTACK-------------------

BLOCK_SIZE = 16

def unpad(data, blocksize=BLOCK_SIZE):
    pad_len = data[-1]
    if data and pad_len < blocksize and data[-pad_len:] == bytes([pad_len]) * pad_len:
        return data[:-pad_len]
    return data

    

def single_block_attack(iv, ciphertext, oracle):
    after_decrypt = b""

    for i in reversed(range(16)):
        padding = bytes([16 - i] * (16 - i))
        for ch in range(256):
            _iv = bytes(i) + xor(padding, bytes([ch]) + after_decrypt)

            if oracle(_iv, ciphertext):
                after_decrypt = bytes([ch]) + after_decrypt
                break

    return xor(iv, after_decrypt)


def full_attack(iv, ciphertext, oracle):
    plaintext = b""

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = single_block_attack(iv, ciphertext[i : i + BLOCK_SIZE], oracle)
        plaintext += block
        iv = ciphertext[i : i + BLOCK_SIZE]
        print(f'Successfully attack block {i // 16 + 1}: {unpad(block, 16).decode()}')

    return plaintext


# -------------------CONNECT AND ATTACK-------------------
context.log_level = "info"  # set debug if need check

HOST = "127.0.0.1"
PORT = 1337
io = remote(HOST, PORT)


def get_data():
    io.recvuntil(b": ")
    given = bytes.fromhex(io.recvline().strip().decode())
    iv, ct = given[:BLOCK_SIZE], given[BLOCK_SIZE:]
    return iv, ct


def check_service(iv, ct):
    send = (iv + ct).hex()
    io.sendlineafter(b": ", send)
    data = io.recvline().strip().decode()
    if "FAIL" in data:
        return False
    elif "Correct!" in data:
        print(data)
    return True


if __name__ == "__main__":
    iv, ct = get_data()
    print("--------Let's break this server!!!--------")
    print(f"This is the initialization vector (hex): {iv.hex()}")
    print(f"This is the ciphertext (hex): {ct.hex()}")

    pt = full_attack(iv, ct, check_service)
    flag = unpad(pt, 16)
    print(f"Here is the recovered data: {flag.decode()}")
